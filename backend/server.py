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

# Create admin router
admin_router = APIRouter(prefix="/api/admin")

# Security
security = HTTPBearer()
JWT_SECRET = "your-super-secret-jwt-key-change-in-production"
JWT_ALGORITHM = "HS256"
ADMIN_JWT_SECRET = "admin-super-secret-jwt-key-change-in-production"

# Admin credentials (in production, store hashed passwords in database)
ADMIN_CREDENTIALS = {
    "admin": "cloudskitchen123",  # username: password
    "manager": "manager123"
}

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
    subcategory: str  # 'north-indian', 'south-indian', 'street-food', 'sweets', 'beverages', 'snacks'
    base_price: float
    customization_options: Dict[str, CustomizationCategory] = Field(default_factory=dict)
    is_active: bool = True
    stock_quantity: int = 100  # Inventory management
    min_stock_level: int = 10
    preparation_time: int = 20  # in minutes
    tags: List[str] = Field(default_factory=list)  # For search functionality
    nutrition_info: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    name: str
    description: str
    images: List[str]
    category: str
    subcategory: str
    base_price: float
    customization_options: Dict[str, CustomizationCategory] = Field(default_factory=dict)
    stock_quantity: int = 100
    min_stock_level: int = 10
    preparation_time: int = 20
    tags: List[str] = Field(default_factory=list)
    nutrition_info: Optional[Dict[str, Any]] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    base_price: Optional[float] = None
    customization_options: Optional[Dict[str, CustomizationCategory]] = None
    is_active: Optional[bool] = None
    stock_quantity: Optional[int] = None
    min_stock_level: Optional[int] = None
    preparation_time: Optional[int] = None
    tags: Optional[List[str]] = None
    nutrition_info: Optional[Dict[str, Any]] = None

# Admin Models
class AdminLogin(BaseModel):
    username: str
    password: str

class AdminTokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str

class ImageUpload(BaseModel):
    filename: str
    image_data: str  # base64 encoded image

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

def create_admin_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=8)  # Shorter expiry for admin
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ADMIN_JWT_SECRET, algorithm=JWT_ALGORITHM)
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

async def get_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, ADMIN_JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in ADMIN_CREDENTIALS:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")
        return {"username": username}
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")

def save_base64_image(image_data: str, filename: str) -> str:
    """Save base64 image data and return the image URL"""
    try:
        # Remove data:image/jpeg;base64, prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(image_data)
        
        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Save image
        image_path = upload_dir / filename
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        
        # Return relative URL (in production, use proper image hosting)
        return f"/uploads/{filename}"
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to save image: {str(e)}")

# Initialize sample data
async def init_sample_data():
    # Check if products already exist
    existing_products = await db.products.count_documents({})
    if existing_products > 0:
        return

    # Import expanded product catalog
    from sample_products import EXPANDED_PRODUCT_CATALOG
    
    # Add all products to database
    for product_data in EXPANDED_PRODUCT_CATALOG:
        product = Product(**product_data)
        await db.products.insert_one(product.dict())

# Admin Authentication Routes
@admin_router.post("/login", response_model=AdminTokenResponse)
async def admin_login(admin_creds: AdminLogin):
    if admin_creds.username not in ADMIN_CREDENTIALS or ADMIN_CREDENTIALS[admin_creds.username] != admin_creds.password:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    
    access_token = create_admin_token(data={"sub": admin_creds.username})
    return AdminTokenResponse(
        access_token=access_token,
        token_type="bearer",
        username=admin_creds.username
    )

@admin_router.get("/verify")
async def verify_admin_token(admin_user=Depends(get_admin_user)):
    return {"valid": True, "username": admin_user["username"]}

# Admin Product Management Routes
@admin_router.get("/products", response_model=List[Product])
async def admin_get_products(
    category: Optional[str] = None,
    active_only: bool = False,
    admin_user=Depends(get_admin_user)
):
    query = {}
    if category:
        query["category"] = category
    if active_only:
        query["is_active"] = True
    
    products = await db.products.find(query).to_list(1000)
    return [Product(**product) for product in products]

@admin_router.get("/products/{product_id}", response_model=Product)
async def admin_get_product(product_id: str, admin_user=Depends(get_admin_user)):
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@admin_router.post("/products", response_model=Product)
async def admin_create_product(product_data: ProductCreate, admin_user=Depends(get_admin_user)):
    product = Product(**product_data.dict())
    await db.products.insert_one(product.dict())
    return product

@admin_router.put("/products/{product_id}", response_model=Product)
async def admin_update_product(
    product_id: str, 
    product_update: ProductUpdate, 
    admin_user=Depends(get_admin_user)
):
    update_data = {k: v for k, v in product_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.products.update_one({"id": product_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updated_product = await db.products.find_one({"id": product_id})
    return Product(**updated_product)

@admin_router.delete("/products/{product_id}")
async def admin_delete_product(product_id: str, admin_user=Depends(get_admin_user)):
    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@admin_router.post("/products/{product_id}/toggle-status")
async def admin_toggle_product_status(product_id: str, admin_user=Depends(get_admin_user)):
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_status = not product["is_active"]
    await db.products.update_one(
        {"id": product_id}, 
        {"$set": {"is_active": new_status, "updated_at": datetime.utcnow()}}
    )
    return {"message": f"Product {'activated' if new_status else 'deactivated'} successfully"}

@admin_router.post("/upload-image")
async def admin_upload_image(image_data: ImageUpload, admin_user=Depends(get_admin_user)):
    try:
        image_url = save_base64_image(image_data.image_data, image_data.filename)
        return {"image_url": image_url, "message": "Image uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Admin Dashboard Stats
@admin_router.get("/stats")
async def admin_get_stats(admin_user=Depends(get_admin_user)):
    total_products = await db.products.count_documents({})
    active_products = await db.products.count_documents({"is_active": True})
    total_orders = await db.orders.count_documents({})
    total_users = await db.users.count_documents({})
    
    # Low stock products
    low_stock_products = await db.products.find({
        "$expr": {"$lte": ["$stock_quantity", "$min_stock_level"]}
    }).to_list(100)
    
    return {
        "total_products": total_products,
        "active_products": active_products,
        "inactive_products": total_products - active_products,
        "total_orders": total_orders,
        "total_users": total_users,
        "low_stock_products": len(low_stock_products),
        "low_stock_items": [Product(**product) for product in low_stock_products]
    }

# Admin Order Management
@admin_router.get("/orders")
async def admin_get_orders(
    status: Optional[str] = None,
    limit: int = 50,
    admin_user=Depends(get_admin_user)
):
    query = {}
    if status:
        query["order_status"] = status
    
    orders = await db.orders.find(query).sort("order_date", -1).limit(limit).to_list(limit)
    return [Order(**order) for order in orders]

@admin_router.put("/orders/{order_id}/status")
async def admin_update_order_status(
    order_id: str, 
    status_data: dict, 
    admin_user=Depends(get_admin_user)
):
    valid_statuses = ["placed", "confirmed", "preparing", "ready", "dispatched", "delivered", "cancelled"]
    new_status = status_data.get("order_status")
    
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid order status")
    
    result = await db.orders.update_one(
        {"id": order_id},
        {"$set": {"order_status": new_status, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order status updated successfully"}

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