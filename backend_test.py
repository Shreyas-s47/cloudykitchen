import requests
import sys
from datetime import datetime
import json

class CloudsKitchenAPITester:
    def __init__(self, base_url="https://1c5c2587-1abe-4e5d-8f3a-e3ddadb5e730.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.admin_api_url = f"{base_url}/api/admin"
        self.token = None
        self.admin_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_user_phone = "9876543210"  # Test phone number as mentioned in requirements
        self.product_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        test_headers = {'Content-Type': 'application/json'}
        
        if headers:
            test_headers.update(headers)
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        print(f"   Method: {method}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, params=data)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, list) and len(response_data) > 0:
                        print(f"   Response: Found {len(response_data)} items")
                    elif isinstance(response_data, dict):
                        print(f"   Response keys: {list(response_data.keys())}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")

            return success, response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test basic health endpoints"""
        print("\n" + "="*50)
        print("TESTING BASIC HEALTH ENDPOINTS")
        print("="*50)
        
        # Test root endpoint
        self.run_test("Root Endpoint", "GET", "", 200)
        
        # Test health endpoint
        self.run_test("Health Check", "GET", "health", 200)

    def test_products_api(self):
        """Test products endpoints"""
        print("\n" + "="*50)
        print("TESTING PRODUCTS API")
        print("="*50)
        
        # Get all products
        success, products = self.run_test("Get All Products", "GET", "products", 200)
        
        if success and products:
            self.product_id = products[0]['id'] if products else None
            print(f"   Found {len(products)} products")
            
            # Test category filtering
            self.run_test("Get Vegetarian Products", "GET", "products", 200, data={"category": "vegetarian"})
            self.run_test("Get Vegan Products", "GET", "products", 200, data={"category": "vegan"})
            
            # Test individual product
            if self.product_id:
                self.run_test("Get Single Product", "GET", f"products/{self.product_id}", 200)
        
        return success

    def test_cart_calculation(self):
        """Test cart calculation endpoint"""
        print("\n" + "="*50)
        print("TESTING CART CALCULATION")
        print("="*50)
        
        # First get a product to test with
        success, products = self.run_test("Get Products for Cart Test", "GET", "products", 200)
        
        if success and products:
            product = products[0]
            
            # Test basic cart calculation
            cart_items = [{
                "product_id": product['id'],
                "quantity": 2,
                "customizations": {},
                "calculated_price": product['base_price'] * 2
            }]
            
            success, cart_response = self.run_test(
                "Calculate Cart Total", 
                "POST", 
                "cart/calculate", 
                200, 
                data=cart_items
            )
            
            if success:
                print(f"   Cart total: ₹{cart_response.get('total_amount', 0)}")
            
            # Test cart with customizations if available
            if product.get('customization_options'):
                customizations = {}
                for category, config in product['customization_options'].items():
                    if config.get('options'):
                        customizations[category] = config['options'][0]['name']
                
                cart_items_custom = [{
                    "product_id": product['id'],
                    "quantity": 1,
                    "customizations": customizations,
                    "calculated_price": product['base_price']
                }]
                
                self.run_test(
                    "Calculate Cart with Customizations", 
                    "POST", 
                    "cart/calculate", 
                    200, 
                    data=cart_items_custom
                )

    def test_authentication_flow(self):
        """Test OTP authentication flow"""
        print("\n" + "="*50)
        print("TESTING AUTHENTICATION FLOW")
        print("="*50)
        
        # Request OTP
        otp_request_data = {"phone": self.test_user_phone}
        success, otp_response = self.run_test(
            "Request OTP", 
            "POST", 
            "auth/request-otp", 
            200, 
            data=otp_request_data
        )
        
        if success and 'otp' in otp_response:
            otp_code = otp_response['otp']
            print(f"   Received OTP: {otp_code}")
            
            # Verify OTP
            verify_data = {
                "phone": self.test_user_phone,
                "otp": otp_code
            }
            
            success, verify_response = self.run_test(
                "Verify OTP", 
                "POST", 
                "auth/verify-otp", 
                200, 
                data=verify_data
            )
            
            if success and 'access_token' in verify_response:
                self.token = verify_response['access_token']
                print(f"   Authentication successful!")
                
                # Test protected endpoint
                self.run_test("Get User Profile", "GET", "users/me", 200)
                
                return True
        
        return False

    def test_order_flow(self):
        """Test order creation (requires authentication)"""
        print("\n" + "="*50)
        print("TESTING ORDER FLOW")
        print("="*50)
        
        if not self.token:
            print("❌ Skipping order tests - no authentication token")
            return False
        
        # Get products for order
        success, products = self.run_test("Get Products for Order", "GET", "products", 200)
        
        if success and products:
            product = products[0]
            
            # Create order data
            order_data = {
                "items": [{
                    "product_id": product['id'],
                    "quantity": 1,
                    "customizations": {},
                    "calculated_price": product['base_price']
                }],
                "delivery_address": {
                    "street": "123 Test Street",
                    "city": "Bangalore",
                    "state": "Karnataka",
                    "pincode": "560001",
                    "landmark": "Near Test Mall"
                },
                "payment_method": "cod"
            }
            
            success, order_response = self.run_test(
                "Create Order", 
                "POST", 
                "orders", 
                200, 
                data=order_data
            )
            
            if success:
                print(f"   Order created successfully!")
                
                # Test get orders
                self.run_test("Get User Orders", "GET", "orders", 200)
                
                return True
        
        return False

    def test_admin_authentication(self):
        """Test admin authentication flow"""
        print("\n" + "="*50)
        print("TESTING ADMIN AUTHENTICATION")
        print("="*50)
        
        # Test admin login with correct credentials
        admin_login_data = {
            "username": "admin",
            "password": "cloudskitchen123"
        }
        
        success, login_response = self.run_test(
            "Admin Login", 
            "POST", 
            f"{self.admin_api_url}/login", 
            200, 
            data=admin_login_data
        )
        
        if success and 'access_token' in login_response:
            self.admin_token = login_response['access_token']
            print(f"   Admin authentication successful!")
            
            # Test admin token verification
            admin_headers = {'Authorization': f'Bearer {self.admin_token}'}
            self.run_test(
                "Verify Admin Token", 
                "GET", 
                f"{self.admin_api_url}/verify", 
                200, 
                headers=admin_headers
            )
            
            return True
        
        return False

    def test_admin_product_management(self):
        """Test admin product CRUD operations"""
        print("\n" + "="*50)
        print("TESTING ADMIN PRODUCT MANAGEMENT")
        print("="*50)
        
        if not self.admin_token:
            print("❌ Skipping admin product tests - no admin token")
            return False
        
        admin_headers = {'Authorization': f'Bearer {self.admin_token}'}
        
        # Test get all products (admin)
        success, products = self.run_test(
            "Admin Get All Products", 
            "GET", 
            f"{self.admin_api_url}/products", 
            200, 
            headers=admin_headers
        )
        
        if success and products:
            print(f"   Found {len(products)} products in admin view")
            
            # Test category filtering
            self.run_test(
                "Admin Get Vegetarian Products", 
                "GET", 
                f"{self.admin_api_url}/products?category=vegetarian", 
                200, 
                headers=admin_headers
            )
            
            self.run_test(
                "Admin Get Vegan Products", 
                "GET", 
                f"{self.admin_api_url}/products?category=vegan", 
                200, 
                headers=admin_headers
            )
            
            # Test get single product
            if products:
                product_id = products[0]['id']
                self.run_test(
                    "Admin Get Single Product", 
                    "GET", 
                    f"{self.admin_api_url}/products/{product_id}", 
                    200, 
                    headers=admin_headers
                )
                
                # Test toggle product status
                self.run_test(
                    "Admin Toggle Product Status", 
                    "POST", 
                    f"{self.admin_api_url}/products/{product_id}/toggle-status", 
                    200, 
                    headers=admin_headers
                )
        
        # Test create new product
        new_product_data = {
            "name": "Test Dish",
            "description": "A test dish for API testing",
            "images": ["https://example.com/test-image.jpg"],
            "category": "vegetarian",
            "subcategory": "north-indian",
            "base_price": 199.0,
            "stock_quantity": 50,
            "min_stock_level": 10,
            "preparation_time": 20,
            "tags": ["test", "api", "dish"]
        }
        
        success, created_product = self.run_test(
            "Admin Create Product", 
            "POST", 
            f"{self.admin_api_url}/products", 
            200, 
            data=new_product_data,
            headers=admin_headers
        )
        
        if success and created_product:
            created_product_id = created_product['id']
            print(f"   Created product with ID: {created_product_id}")
            
            # Test update product
            update_data = {
                "name": "Updated Test Dish",
                "base_price": 249.0
            }
            
            self.run_test(
                "Admin Update Product", 
                "PUT", 
                f"{self.admin_api_url}/products/{created_product_id}", 
                200, 
                data=update_data,
                headers=admin_headers
            )
            
            # Test delete product
            self.run_test(
                "Admin Delete Product", 
                "DELETE", 
                f"{self.admin_api_url}/products/{created_product_id}", 
                200, 
                headers=admin_headers
            )
        
        return True

    def test_admin_stats_dashboard(self):
        """Test admin stats and dashboard endpoints"""
        print("\n" + "="*50)
        print("TESTING ADMIN STATS & DASHBOARD")
        print("="*50)
        
        if not self.admin_token:
            print("❌ Skipping admin stats tests - no admin token")
            return False
        
        admin_headers = {'Authorization': f'Bearer {self.admin_token}'}
        
        # Test admin stats
        success, stats = self.run_test(
            "Admin Get Stats", 
            "GET", 
            f"{self.admin_api_url}/stats", 
            200, 
            headers=admin_headers
        )
        
        if success and stats:
            print(f"   Total products: {stats.get('total_products', 0)}")
            print(f"   Active products: {stats.get('active_products', 0)}")
            print(f"   Total users: {stats.get('total_users', 0)}")
            print(f"   Total orders: {stats.get('total_orders', 0)}")
            print(f"   Low stock products: {stats.get('low_stock_products', 0)}")
        
        return True

    def test_admin_order_management(self):
        """Test admin order management"""
        print("\n" + "="*50)
        print("TESTING ADMIN ORDER MANAGEMENT")
        print("="*50)
        
        if not self.admin_token:
            print("❌ Skipping admin order tests - no admin token")
            return False
        
        admin_headers = {'Authorization': f'Bearer {self.admin_token}'}
        
        # Test get all orders
        success, orders = self.run_test(
            "Admin Get All Orders", 
            "GET", 
            f"{self.admin_api_url}/orders", 
            200, 
            headers=admin_headers
        )
        
        if success:
            print(f"   Found {len(orders) if orders else 0} orders")
            
            # If there are orders, test status update
            if orders and len(orders) > 0:
                order_id = orders[0]['id']
                status_update = {"order_status": "confirmed"}
                
                self.run_test(
                    "Admin Update Order Status", 
                    "PUT", 
                    f"{self.admin_api_url}/orders/{order_id}/status", 
                    200, 
                    data=status_update,
                    headers=admin_headers
                )
        
        return True

    def test_product_data_structure(self):
        """Test that products have all required new fields"""
        print("\n" + "="*50)
        print("TESTING PRODUCT DATA STRUCTURE")
        print("="*50)
        
        # Get all products and verify structure
        success, products = self.run_test("Get Products for Structure Test", "GET", "products", 200)
        
        if success and products:
            print(f"   Testing data structure of {len(products)} products")
            
            # Check first product for required fields
            if products:
                product = products[0]
                required_fields = [
                    'id', 'name', 'description', 'images', 'category', 'subcategory',
                    'base_price', 'stock_quantity', 'min_stock_level', 'preparation_time',
                    'tags', 'is_active', 'created_at', 'updated_at'
                ]
                
                missing_fields = []
                for field in required_fields:
                    if field not in product:
                        missing_fields.append(field)
                
                if not missing_fields:
                    print("✅ All required fields present in product data")
                    self.tests_passed += 1
                else:
                    print(f"❌ Missing fields: {missing_fields}")
                
                self.tests_run += 1
                
                # Check subcategories
                subcategories = set()
                categories = set()
                for p in products:
                    subcategories.add(p.get('subcategory', 'unknown'))
                    categories.add(p.get('category', 'unknown'))
                
                print(f"   Categories found: {sorted(categories)}")
                print(f"   Subcategories found: {sorted(subcategories)}")
        
        return success

    def test_error_handling(self):
        """Test error handling scenarios"""
        print("\n" + "="*50)
        print("TESTING ERROR HANDLING")
        print("="*50)
        
        # Test invalid product ID
        self.run_test("Get Invalid Product", "GET", "products/invalid-id", 404)
        
        # Test invalid OTP
        invalid_otp_data = {
            "phone": self.test_user_phone,
            "otp": "000000"
        }
        self.run_test("Verify Invalid OTP", "POST", "auth/verify-otp", 400, data=invalid_otp_data)
        
        # Test cart calculation with invalid product
        invalid_cart = [{
            "product_id": "invalid-product-id",
            "quantity": 1,
            "customizations": {},
            "calculated_price": 100
        }]
        self.run_test("Calculate Cart with Invalid Product", "POST", "cart/calculate", 404, data=invalid_cart)
        
        # Test admin login with invalid credentials
        invalid_admin_data = {
            "username": "invalid",
            "password": "invalid"
        }
        self.run_test("Invalid Admin Login", "POST", f"{self.admin_api_url}/login", 401, data=invalid_admin_data)

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Clouds Kitchen API Tests")
        print(f"🌐 Testing against: {self.base_url}")
        
        # Run test suites
        self.test_health_check()
        self.test_products_api()
        self.test_cart_calculation()
        auth_success = self.test_authentication_flow()
        
        if auth_success:
            self.test_order_flow()
        
        self.test_error_handling()
        
        # Print final results
        print("\n" + "="*60)
        print("FINAL TEST RESULTS")
        print("="*60)
        print(f"📊 Tests passed: {self.tests_passed}/{self.tests_run}")
        print(f"📈 Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed")
            return 1

def main():
    tester = CloudsKitchenAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())