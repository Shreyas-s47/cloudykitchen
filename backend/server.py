from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import uuid
from datetime import datetime, timedelta
import jwt
import bcrypt
import random
import string
import re
import base64
import io
from PIL import Image

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Clouds Kitchen API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()
JWT_SECRET = "your-super-secret-jwt-key-change-in-production"
JWT_ALGORITHM = "HS256"

# Models
class CustomizationOption(BaseModel):
    name: str
    price_modifier: float = 0.0

class CustomizationCategory(BaseModel):
    enabled: bool = True
    options: List[CustomizationOption]

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    images: List[str]
    category: str  # 'vegan' or 'vegetarian'
    base_price: float
    customization_options: Dict[str, CustomizationCategory] = Field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    name: str
    description: str
    images: List[str]
    category: str
    base_price: float
    customization_options: Dict[str, CustomizationCategory] = Field(default_factory=dict)

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    category: Optional[str] = None
    base_price: Optional[float] = None
    customization_options: Optional[Dict[str, CustomizationCategory]] = None
    is_active: Optional[bool] = None

class CartItem(BaseModel):
    product_id: str
    quantity: int
    customizations: Dict[str, str] = Field(default_factory=dict)
    calculated_price: float

class CartResponse(BaseModel):
    items: List[CartItem]
    total_amount: float

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: Optional[str] = None
    phone: Optional[str] = None
    name: str
    addresses: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    name: str

class OTPRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None

class OTPVerify(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    otp: str

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[CartItem]
    total_amount: float
    delivery_address: Dict[str, Any]
    payment_method: str = "cod"
    payment_status: str = "pending"
    order_status: str = "placed"
    order_date: datetime = Field(default_factory=datetime.utcnow)
    delivery_date: Optional[datetime] = None

class OrderCreate(BaseModel):
    items: List[CartItem]
    delivery_address: Dict[str, Any]
    payment_method: str = "cod"

# Helper Functions
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = await db.users.find_one({"id": user_id})
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return User(**user)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Initialize sample data
async def init_sample_data():
    # Check if products already exist
    existing_products = await db.products.count_documents({})
    if existing_products > 0:
        return

    # Sample vegetarian and vegan products with customization options
    sample_products = [
        # Vegan Products
        {
            "name": "Buddha Bowl Delight",
            "description": "A colorful and nutritious vegan bowl packed with quinoa, roasted vegetables, avocado, and tahini dressing",
            "images": ["https://images.unsplash.com/photo-1599020792689-9fde458e7e17?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHx2ZWdldGFyaWFuJTIwZm9vZHxlbnwwfHx8fDE3NTQyMTExMTd8MA&ixlib=rb-4.1.0&q=85"],
            "category": "vegan",
            "base_price": 299.0,
            "customization_options": {
                "base": {
                    "enabled": True,
                    "options": [
                        {"name": "Quinoa", "price_modifier": 0},
                        {"name": "Brown Rice", "price_modifier": -20},
                        {"name": "Mixed Grains", "price_modifier": 15}
                    ]
                },
                "protein": {
                    "enabled": True,
                    "options": [
                        {"name": "Tofu", "price_modifier": 0},
                        {"name": "Tempeh", "price_modifier": 25},
                        {"name": "Chickpeas", "price_modifier": -10}
                    ]
                },
                "dressing": {
                    "enabled": True,
                    "options": [
                        {"name": "Tahini", "price_modifier": 0},
                        {"name": "Hummus", "price_modifier": 10},
                        {"name": "Avocado Cream", "price_modifier": 20}
                    ]
                }
            }
        },
        {
            "name": "Vegan Power Bowl",
            "description": "Energizing vegan bowl with plant-based protein, fresh greens, and superfood toppings",
            "images": ["https://images.unsplash.com/photo-1598449426314-8b02525e8733?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHx2ZWdldGFyaWFuJTIwZm9vZHxlbnwwfHx8fDE3NTQyMTExMTd8MA&ixlib=rb-4.1.0&q=85"],
            "category": "vegan",
            "base_price": 329.0,
            "customization_options": {
                "greens": {
                    "enabled": True,
                    "options": [
                        {"name": "Spinach", "price_modifier": 0},
                        {"name": "Kale", "price_modifier": 10},
                        {"name": "Mixed Greens", "price_modifier": 15}
                    ]
                },
                "nuts": {
                    "enabled": True,
                    "options": [
                        {"name": "Almonds", "price_modifier": 0},
                        {"name": "Walnuts", "price_modifier": 10},
                        {"name": "Cashews", "price_modifier": 15}
                    ]
                }
            }
        },
        {
            "name": "Cauliflower & Hazelnut Salad",
            "description": "Roasted cauliflower with crunchy hazelnuts and fresh herbs in a zesty lemon dressing",
            "images": ["https://images.unsplash.com/photo-1588930850267-fe671c9ed91f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwyfHx2ZWdhbiUyMGRpc2hlc3xlbnwwfHx8fDE3NTQyMTExMjN8MA&ixlib=rb-4.1.0&q=85"],
            "category": "vegan",
            "base_price": 249.0,
            "customization_options": {
                "roast_level": {
                    "enabled": True,
                    "options": [
                        {"name": "Light Roast", "price_modifier": 0},
                        {"name": "Medium Roast", "price_modifier": 0},
                        {"name": "Deep Roast", "price_modifier": 5}
                    ]
                },
                "nuts": {
                    "enabled": True,
                    "options": [
                        {"name": "Hazelnuts", "price_modifier": 0},
                        {"name": "Almonds", "price_modifier": -5},
                        {"name": "Mixed Nuts", "price_modifier": 10}
                    ]
                }
            }
        },
        # Vegetarian Products
        {
            "name": "Traditional Tamil Thali",
            "description": "Authentic South Indian thali with rice, dal, vegetables, pickles, and traditional accompaniments",
            "images": ["https://images.unsplash.com/photo-1742281258189-3b933879867a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHwyfHxpbmRpYW4lMjB2ZWdldGFyaWFufGVufDB8fHx8MTc1NDIxMTEyN3ww&ixlib=rb-4.1.0&q=85"],
            "category": "vegetarian",
            "base_price": 349.0,
            "customization_options": {
                "rice": {
                    "enabled": True,
                    "options": [
                        {"name": "White Rice", "price_modifier": 0},
                        {"name": "Brown Rice", "price_modifier": 10},
                        {"name": "Jeera Rice", "price_modifier": 15}
                    ]
                },
                "dal": {
                    "enabled": True,
                    "options": [
                        {"name": "Toor Dal", "price_modifier": 0},
                        {"name": "Moong Dal", "price_modifier": 5},
                        {"name": "Mixed Dal", "price_modifier": 10}
                    ]
                },
                "spice_level": {
                    "enabled": True,
                    "options": [
                        {"name": "Mild", "price_modifier": 0},
                        {"name": "Medium", "price_modifier": 0},
                        {"name": "Spicy", "price_modifier": 0}
                    ]
                }
            }
        },
        {
            "name": "Festival Special Thali",
            "description": "Elaborate vegetarian thali with seasonal vegetables, special sweets, and festive preparations",
            "images": ["https://images.unsplash.com/photo-1742281257687-092746ad6021?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHwzfHxpbmRpYW4lMjB2ZWdldGFyaWFufGVufDB8fHx8MTc1NDIxMTEyN3ww&ixlib=rb-4.1.0&q=85"],
            "category": "vegetarian",
            "base_price": 449.0,
            "customization_options": {
                "sweet": {
                    "enabled": True,
                    "options": [
                        {"name": "Kheer", "price_modifier": 0},
                        {"name": "Gulab Jamun", "price_modifier": 10},
                        {"name": "Rasmalai", "price_modifier": 15}
                    ]
                },
                "vegetable_curry": {
                    "enabled": True,
                    "options": [
                        {"name": "Mixed Vegetables", "price_modifier": 0},
                        {"name": "Paneer Curry", "price_modifier": 25},
                        {"name": "Palak Paneer", "price_modifier": 30}
                    ]
                }
            }
        },
        {
            "name": "Complete Indian Thali",
            "description": "Full traditional Indian meal with rice, bread, vegetables, dal, yogurt, and pickles",
            "images": ["https://images.unsplash.com/photo-1742281257707-0c7f7e5ca9c6?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHw0fHxpbmRpYW4lMjB2ZWdldGFyaWFufGVufDB8fHx8MTc1NDIxMTEyN3ww&ixlib=rb-4.1.0&q=85"],
            "category": "vegetarian",
            "base_price": 399.0,
            "customization_options": {
                "bread": {
                    "enabled": True,
                    "options": [
                        {"name": "Chapati", "price_modifier": 0},
                        {"name": "Naan", "price_modifier": 15},
                        {"name": "Paratha", "price_modifier": 20}
                    ]
                },
                "yogurt": {
                    "enabled": True,
                    "options": [
                        {"name": "Plain Yogurt", "price_modifier": 0},
                        {"name": "Raita", "price_modifier": 10},
                        {"name": "Buttermilk", "price_modifier": 5}
                    ]
                }
            }
        },
        # More products
        {
            "name": "Fresh Garden Salad",
            "description": "Crisp mixed greens with seasonal vegetables, nuts, and house-made dressing",
            "images": ["https://images.unsplash.com/photo-1615366105533-5b8f3255ea5d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwzfHx2ZWdldGFyaWFuJTIwZm9vZHxlbnwwfHx8fDE3NTQyMTExMTd8MA&ixlib=rb-4.1.0&q=85"],
            "category": "vegan",
            "base_price": 199.0,
            "customization_options": {
                "dressing": {
                    "enabled": True,
                    "options": [
                        {"name": "Olive Oil & Lemon", "price_modifier": 0},
                        {"name": "Balsamic Vinaigrette", "price_modifier": 5},
                        {"name": "Tahini Dressing", "price_modifier": 10}
                    ]
                }
            }
        },
        {
            "name": "Protein-Rich Salad Bowl",
            "description": "Nutritious salad with plant-based proteins, fresh vegetables, and superfood toppings",
            "images": ["https://images.unsplash.com/photo-1512621776951-a57141f2eefd?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHw0fHx2ZWdldGFyaWFuJTIwZm9vZHxlbnwwfHx8fDE3NTQyMTExMTd8MA&ixlib=rb-4.1.0&q=85"],
            "category": "vegan",
            "base_price": 279.0,
            "customization_options": {
                "protein": {
                    "enabled": True,
                    "options": [
                        {"name": "Grilled Tofu", "price_modifier": 0},
                        {"name": "Tempeh", "price_modifier": 20},
                        {"name": "Lentils", "price_modifier": -10}
                    ]
                }
            }
        }
    ]

    for product_data in sample_products:
        product = Product(**product_data)
        await db.products.insert_one(product.dict())

# Product routes
@api_router.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None, active_only: bool = True):
    query = {}
    if category:
        query["category"] = category
    if active_only:
        query["is_active"] = True
    
    products = await db.products.find(query).to_list(1000)
    return [Product(**product) for product in products]

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@api_router.post("/products", response_model=Product)
async def create_product(product_data: ProductCreate):
    product = Product(**product_data.dict())
    await db.products.insert_one(product.dict())
    return product

@api_router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_update: ProductUpdate):
    update_data = {k: v for k, v in product_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.products.update_one({"id": product_id}, {"$set": update_data})
    updated_product = await db.products.find_one({"id": product_id})
    
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**updated_product)

@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Cart routes (guest cart calculation)
@api_router.post("/cart/calculate", response_model=CartResponse)
async def calculate_cart(items: List[CartItem]):
    total = 0.0
    calculated_items = []
    
    for item in items:
        # Get product details
        product = await db.products.find_one({"id": item.product_id})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        product_obj = Product(**product)
        item_price = product_obj.base_price
        
        # Calculate customization price
        for category, option in item.customizations.items():
            if category in product_obj.customization_options:
                for opt in product_obj.customization_options[category].options:
                    if opt.name == option:
                        item_price += opt.price_modifier
                        break
        
        calculated_price = item_price * item.quantity
        calculated_item = CartItem(
            product_id=item.product_id,
            quantity=item.quantity,
            customizations=item.customizations,
            calculated_price=calculated_price
        )
        calculated_items.append(calculated_item)
        total += calculated_price
    
    return CartResponse(items=calculated_items, total_amount=total)

# Authentication routes
@api_router.post("/auth/request-otp")
async def request_otp(otp_request: OTPRequest):
    if not otp_request.email and not otp_request.phone:
        raise HTTPException(status_code=400, detail="Either email or phone is required")
    
    otp = generate_otp()
    
    # Store OTP in database (in production, use Redis for better performance)
    otp_data = {
        "otp": otp,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=10),
        "verified": False
    }
    
    if otp_request.email:
        otp_data["email"] = otp_request.email
        # TODO: Send email OTP (implement with actual email service)
        logger.info(f"OTP for email {otp_request.email}: {otp}")
    
    if otp_request.phone:
        otp_data["phone"] = otp_request.phone
        # TODO: Send SMS OTP (implement with actual SMS service)
        logger.info(f"OTP for phone {otp_request.phone}: {otp}")
    
    await db.otp_codes.insert_one(otp_data)
    
    return {"message": "OTP sent successfully", "otp": otp}  # Remove otp in production

@api_router.post("/auth/verify-otp")
async def verify_otp(otp_verify: OTPVerify):
    query = {"otp": otp_verify.otp, "verified": False}
    
    if otp_verify.email:
        query["email"] = otp_verify.email
    if otp_verify.phone:
        query["phone"] = otp_verify.phone
    
    otp_record = await db.otp_codes.find_one(query)
    
    if not otp_record or otp_record["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    # Mark OTP as verified
    await db.otp_codes.update_one({"_id": otp_record["_id"]}, {"$set": {"verified": True}})
    
    # Check if user exists or create new user
    user_query = {}
    if otp_verify.email:
        user_query["email"] = otp_verify.email
    if otp_verify.phone:
        user_query["phone"] = otp_verify.phone
    
    user = await db.users.find_one(user_query)
    
    if not user:
        # Create new user
        user_data = {
            "name": "New User",  # Will be updated during profile completion
        }
        if otp_verify.email:
            user_data["email"] = otp_verify.email
        if otp_verify.phone:
            user_data["phone"] = otp_verify.phone
        
        new_user = User(**user_data)
        await db.users.insert_one(new_user.dict())
        user = new_user.dict()
    
    # Create JWT token
    access_token = create_access_token(data={"sub": user["id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": User(**user)
    }

# User routes
@api_router.get("/users/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@api_router.put("/users/me", response_model=User)
async def update_user_profile(
    user_update: dict,
    current_user: User = Depends(get_current_user)
):
    user_update["updated_at"] = datetime.utcnow()
    
    await db.users.update_one({"id": current_user.id}, {"$set": user_update})
    updated_user = await db.users.find_one({"id": current_user.id})
    
    return User(**updated_user)

# Order routes
@api_router.post("/orders", response_model=Order)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user)
):
    order = Order(
        user_id=current_user.id,
        items=order_data.items,
        total_amount=sum(item.calculated_price for item in order_data.items),
        delivery_address=order_data.delivery_address,
        payment_method=order_data.payment_method
    )
    
    await db.orders.insert_one(order.dict())
    return order

@api_router.get("/orders", response_model=List[Order])
async def get_user_orders(current_user: User = Depends(get_current_user)):
    orders = await db.orders.find({"user_id": current_user.id}).to_list(1000)
    return [Order(**order) for order in orders]

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_user)
):
    order = await db.orders.find_one({"id": order_id, "user_id": current_user.id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**order)

# Admin routes (simplified for MVP)
@api_router.get("/admin/orders", response_model=List[Order])
async def get_all_orders():
    orders = await db.orders.find().to_list(1000)
    return [Order(**orders) for order in orders]

@api_router.put("/admin/orders/{order_id}/status")
async def update_order_status(order_id: str, status: dict):
    await db.orders.update_one(
        {"id": order_id},
        {"$set": {"order_status": status["order_status"], "updated_at": datetime.utcnow()}}
    )
    return {"message": "Order status updated"}

# Basic routes
@api_router.get("/")
async def root():
    return {"message": "Welcome to Clouds Kitchen API"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    # Initialize sample data
    await init_sample_data()
    logger.info("Sample data initialized")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()