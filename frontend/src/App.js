import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import { Button } from './components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Badge } from './components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './components/ui/dialog';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Textarea } from './components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { toast } from 'sonner';
import { Toaster } from './components/ui/sonner';
import { ShoppingCart, Plus, Minus, Heart, Star, Leaf, User, MapPin, Phone, Mail, Search, Filter } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Context for cart and auth
const AppContext = React.createContext();

function App() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Load cart from localStorage
  useEffect(() => {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      setCart(JSON.parse(savedCart));
    }
  }, []);

  // Save cart to localStorage
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  // Load user info if token exists
  useEffect(() => {
    if (token) {
      loadUserInfo();
    }
  }, [token]);

  // Load products
  useEffect(() => {
    loadProducts();
  }, [selectedCategory]);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const params = selectedCategory !== 'all' ? { category: selectedCategory } : {};
      const response = await axios.get(`${API}/products`, { params });
      setProducts(response.data);
    } catch (error) {
      console.error('Failed to load products:', error);
      toast.error('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const loadUserInfo = async () => {
    try {
      const response = await axios.get(`${API}/users/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(response.data);
    } catch (error) {
      console.error('Failed to load user info:', error);
      // Token might be invalid, clear it
      localStorage.removeItem('token');
      setToken(null);
    }
  };

  const addToCart = (product, customizations = {}, quantity = 1) => {
    const cartItem = {
      product_id: product.id,
      product,
      quantity,
      customizations,
      calculated_price: calculateItemPrice(product, customizations, quantity)
    };
    
    setCart(prev => {
      const existingIndex = prev.findIndex(item => 
        item.product_id === product.id && 
        JSON.stringify(item.customizations) === JSON.stringify(customizations)
      );
      
      if (existingIndex >= 0) {
        const updated = [...prev];
        updated[existingIndex].quantity += quantity;
        updated[existingIndex].calculated_price = calculateItemPrice(
          product, customizations, updated[existingIndex].quantity
        );
        return updated;
      }
      
      return [...prev, cartItem];
    });
    
    toast.success('Added to cart!');
  };

  const updateCartQuantity = (index, newQuantity) => {
    if (newQuantity === 0) {
      removeFromCart(index);
      return;
    }
    
    setCart(prev => {
      const updated = [...prev];
      updated[index].quantity = newQuantity;
      updated[index].calculated_price = calculateItemPrice(
        updated[index].product,
        updated[index].customizations,
        newQuantity
      );
      return updated;
    });
  };

  const removeFromCart = (index) => {
    setCart(prev => prev.filter((_, i) => i !== index));
    toast.success('Removed from cart');
  };

  const calculateItemPrice = (product, customizations, quantity) => {
    let price = product.base_price;
    
    Object.entries(customizations).forEach(([category, option]) => {
      if (product.customization_options[category]) {
        const optionData = product.customization_options[category].options.find(
          opt => opt.name === option
        );
        if (optionData) {
          price += optionData.price_modifier;
        }
      }
    });
    
    return price * quantity;
  };

  const getCartTotal = () => {
    return cart.reduce((sum, item) => sum + item.calculated_price, 0);
  };

  const contextValue = {
    products,
    cart,
    user,
    token,
    setToken: (newToken) => {
      setToken(newToken);
      if (newToken) {
        localStorage.setItem('token', newToken);
      } else {
        localStorage.removeItem('token');
        setUser(null);
      }
    },
    addToCart,
    updateCartQuantity,
    removeFromCart,
    getCartTotal,
    loadProducts,
    loadUserInfo
  };

  return (
    <AppContext.Provider value={contextValue}>
      <div className="min-h-screen bg-gradient-to-b from-orange-50 to-green-50">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage selectedCategory={selectedCategory} setSelectedCategory={setSelectedCategory} loading={loading} />} />
            <Route path="/product/:id" element={<ProductDetailPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/admin/*" element={<AdminRoutes />} />
          </Routes>
        </BrowserRouter>
        <Toaster />
      </div>
    </AppContext.Provider>
  );
}

// HomePage Component
function HomePage({ selectedCategory, setSelectedCategory, loading }) {
  const { products } = React.useContext(AppContext);

  return (
    <>
      <Header />
      <HeroSection />
      <div className="container mx-auto px-4 py-8">
        <CategoryFilter selectedCategory={selectedCategory} setSelectedCategory={setSelectedCategory} />
        <ProductGrid products={products} loading={loading} />
      </div>
      <Footer />
    </>
  );
}

// Header Component
function Header() {
  const { cart, user } = React.useContext(AppContext);
  const [showAuth, setShowAuth] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b border-green-100">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-orange-500 rounded-full flex items-center justify-center">
              <Leaf className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Clouds Kitchen</h1>
              <p className="text-sm text-gray-600">Pure Vegetarian & Vegan Delights</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              className="relative"
              onClick={() => window.location.href = '/cart'}
            >
              <ShoppingCart className="w-5 h-5 mr-2" />
              Cart
              {cart.length > 0 && (
                <Badge className="absolute -top-2 -right-2 bg-orange-500 text-white">
                  {cart.length}
                </Badge>
              )}
            </Button>
            
            {user ? (
              <Button
                variant="outline"
                onClick={() => window.location.href = '/profile'}
              >
                <User className="w-5 h-5 mr-2" />
                {user.name}
              </Button>
            ) : (
              <Button
                onClick={() => setShowAuth(true)}
                className="bg-green-600 hover:bg-green-700"
              >
                Sign In
              </Button>
            )}
          </div>
        </div>
      </div>
      
      {showAuth && <AuthModal onClose={() => setShowAuth(false)} />}
    </header>
  );
}

// Hero Section
function HeroSection() {
  return (
    <section className="bg-gradient-to-r from-green-600 via-green-700 to-orange-600 text-white py-20">
      <div className="container mx-auto px-4 text-center">
        <h2 className="text-5xl font-bold mb-6">
          Authentic Vegetarian & Vegan Cuisine
        </h2>
        <p className="text-xl mb-8 opacity-90">
          Celebrating the rich flavors of plant-based cooking with traditional and modern dishes
        </p>
        <div className="flex flex-wrap justify-center gap-4 text-sm">
          <Badge className="bg-white/20 text-white border-white/30">100% Vegetarian</Badge>
          <Badge className="bg-white/20 text-white border-white/30">Fresh Daily</Badge>
          <Badge className="bg-white/20 text-white border-white/30">Traditional Recipes</Badge>
          <Badge className="bg-white/20 text-white border-white/30">Festival Specials</Badge>
        </div>
      </div>
    </section>
  );
}

// Category Filter
function CategoryFilter({ selectedCategory, setSelectedCategory }) {
  const categories = [
    { key: 'all', label: 'All Items', icon: '🍽️' },
    { key: 'vegetarian', label: 'Vegetarian', icon: '🥗' },
    { key: 'vegan', label: 'Vegan', icon: '🌱' }
  ];

  return (
    <div className="mb-8">
      <div className="flex flex-wrap gap-4 justify-center">
        {categories.map(category => (
          <Button
            key={category.key}
            variant={selectedCategory === category.key ? 'default' : 'outline'}
            onClick={() => setSelectedCategory(category.key)}
            className={`px-6 py-3 ${
              selectedCategory === category.key 
                ? 'bg-green-600 text-white' 
                : 'border-green-200 text-green-700 hover:bg-green-50'
            }`}
          >
            <span className="mr-2">{category.icon}</span>
            {category.label}
          </Button>
        ))}
      </div>
    </div>
  );
}

// Product Grid
function ProductGrid({ products, loading }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <Card key={i} className="animate-pulse">
            <div className="h-48 bg-gray-200 rounded-t-lg"></div>
            <CardContent className="p-4">
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (!products.length) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No products found in this category</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

// Product Card
function ProductCard({ product }) {
  const { addToCart } = React.useContext(AppContext);
  const [showCustomization, setShowCustomization] = useState(false);

  const hasCustomizations = product.customization_options && 
    Object.keys(product.customization_options).length > 0;

  const handleAddToCart = () => {
    if (hasCustomizations) {
      setShowCustomization(true);
    } else {
      addToCart(product);
    }
  };

  return (
    <>
      <Card className="group overflow-hidden border-green-100 hover:border-green-300 hover:shadow-lg transition-all duration-300">
        <div className="relative overflow-hidden">
          <img
            src={product.images[0]}
            alt={product.name}
            className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <Badge 
            className={`absolute top-3 right-3 ${
              product.category === 'vegan' 
                ? 'bg-green-600 text-white' 
                : 'bg-orange-600 text-white'
            }`}
          >
            {product.category === 'vegan' ? '🌱 Vegan' : '🥛 Vegetarian'}
          </Badge>
        </div>
        
        <CardContent className="p-4">
          <div className="flex justify-between items-start mb-2">
            <h3 className="font-semibold text-lg text-gray-900 line-clamp-2">{product.name}</h3>
            <div className="flex items-center text-yellow-500 ml-2">
              <Star className="w-4 h-4 fill-current" />
              <span className="text-sm ml-1">4.5</span>
            </div>
          </div>
          
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">{product.description}</p>
          
          <div className="flex justify-between items-center">
            <div className="text-2xl font-bold text-green-600">₹{product.base_price}</div>
            <Button 
              onClick={handleAddToCart}
              className="bg-green-600 hover:bg-green-700 text-white"
            >
              <Plus className="w-4 h-4 mr-1" />
              Add
            </Button>
          </div>
          
          {hasCustomizations && (
            <p className="text-xs text-gray-500 mt-2">✨ Customization available</p>
          )}
        </CardContent>
      </Card>

      {showCustomization && (
        <CustomizationModal
          product={product}
          onClose={() => setShowCustomization(false)}
        />
      )}
    </>
  );
}

// Customization Modal
function CustomizationModal({ product, onClose }) {
  const { addToCart } = React.useContext(AppContext);
  const [customizations, setCustomizations] = useState({});
  const [quantity, setQuantity] = useState(1);

  const calculatePrice = () => {
    let price = product.base_price;
    Object.entries(customizations).forEach(([category, option]) => {
      if (product.customization_options[category]) {
        const optionData = product.customization_options[category].options.find(
          opt => opt.name === option
        );
        if (optionData) {
          price += optionData.price_modifier;
        }
      }
    });
    return price * quantity;
  };

  const handleAddToCart = () => {
    addToCart(product, customizations, quantity);
    onClose();
  };

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-md max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <img src={product.images[0]} alt={product.name} className="w-8 h-8 rounded" />
            Customize {product.name}
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          {Object.entries(product.customization_options).map(([category, config]) => (
            <div key={category}>
              <Label className="text-sm font-medium capitalize mb-2 block">
                {category.replace('_', ' ')}
              </Label>
              <Select
                value={customizations[category] || ''}
                onValueChange={(value) =>
                  setCustomizations(prev => ({ ...prev, [category]: value }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder={`Choose ${category}`} />
                </SelectTrigger>
                <SelectContent>
                  {config.options.map(option => (
                    <SelectItem key={option.name} value={option.name}>
                      <div className="flex justify-between w-full">
                        <span>{option.name}</span>
                        {option.price_modifier !== 0 && (
                          <span className="ml-2 text-green-600">
                            {option.price_modifier > 0 ? '+' : ''}₹{option.price_modifier}
                          </span>
                        )}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          ))}
          
          <div>
            <Label className="text-sm font-medium mb-2 block">Quantity</Label>
            <div className="flex items-center gap-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                disabled={quantity <= 1}
              >
                <Minus className="w-4 h-4" />
              </Button>
              <span className="font-medium">{quantity}</span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setQuantity(quantity + 1)}
              >
                <Plus className="w-4 h-4" />
              </Button>
            </div>
          </div>
          
          <div className="border-t pt-4">
            <div className="flex justify-between items-center mb-4">
              <span className="font-medium">Total Price:</span>
              <span className="text-2xl font-bold text-green-600">₹{calculatePrice()}</span>
            </div>
            
            <Button onClick={handleAddToCart} className="w-full bg-green-600 hover:bg-green-700">
              Add to Cart - ₹{calculatePrice()}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

// Cart Page
function CartPage() {
  const { cart, updateCartQuantity, removeFromCart, getCartTotal } = React.useContext(AppContext);

  if (cart.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="container mx-auto px-4 py-8">
          <div className="text-center py-12">
            <ShoppingCart className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Your cart is empty</h2>
            <p className="text-gray-600 mb-6">Add some delicious items to get started</p>
            <Button 
              onClick={() => window.location.href = '/'}
              className="bg-green-600 hover:bg-green-700"
            >
              Continue Shopping
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Your Cart</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-4">
            {cart.map((item, index) => (
              <Card key={index}>
                <CardContent className="p-4">
                  <div className="flex items-center gap-4">
                    <img
                      src={item.product.images[0]}
                      alt={item.product.name}
                      className="w-20 h-20 rounded-lg object-cover"
                    />
                    
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">{item.product.name}</h3>
                      <Badge className={`mb-2 ${
                        item.product.category === 'vegan' 
                          ? 'bg-green-100 text-green-700' 
                          : 'bg-orange-100 text-orange-700'
                      }`}>
                        {item.product.category}
                      </Badge>
                      
                      {Object.keys(item.customizations).length > 0 && (
                        <div className="text-sm text-gray-600">
                          {Object.entries(item.customizations).map(([key, value]) => (
                            <div key={key}>
                              <span className="capitalize">{key.replace('_', ' ')}: </span>
                              <span className="font-medium">{value}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <div className="flex flex-col items-end gap-3">
                      <div className="text-xl font-bold text-green-600">
                        ₹{item.calculated_price}
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => updateCartQuantity(index, item.quantity - 1)}
                        >
                          <Minus className="w-4 h-4" />
                        </Button>
                        <span className="font-medium px-2">{item.quantity}</span>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => updateCartQuantity(index, item.quantity + 1)}
                        >
                          <Plus className="w-4 h-4" />
                        </Button>
                      </div>
                      
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => removeFromCart(index)}
                        className="text-red-600 hover:text-red-700"
                      >
                        Remove
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
          
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Order Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span>Subtotal ({cart.length} items)</span>
                    <span>₹{getCartTotal()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Delivery Fee</span>
                    <span className="text-green-600">FREE</span>
                  </div>
                  <div className="border-t pt-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xl font-bold">Total</span>
                      <span className="text-xl font-bold text-green-600">₹{getCartTotal()}</span>
                    </div>
                  </div>
                </div>
                
                <Button 
                  className="w-full mt-6 bg-green-600 hover:bg-green-700"
                  onClick={() => window.location.href = '/checkout'}
                >
                  Proceed to Checkout
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

// Product Detail Page
function ProductDetailPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-semibold mb-4">Product Details</h2>
          <p className="text-gray-600">Product detail page coming soon...</p>
          <Button 
            onClick={() => window.location.href = '/'}
            className="mt-4 bg-green-600 hover:bg-green-700"
          >
            Back to Home
          </Button>
        </div>
      </div>
    </div>
  );
}
function AuthModal({ onClose }) {
  const { setToken, loadUserInfo } = React.useContext(AppContext);
  const [step, setStep] = useState('request'); // 'request' or 'verify'
  const [contact, setContact] = useState('');
  const [otp, setOTP] = useState('');
  const [contactType, setContactType] = useState('phone'); // 'phone' or 'email'
  const [loading, setLoading] = useState(false);

  const requestOTP = async () => {
    if (!contact.trim()) {
      toast.error('Please enter your contact information');
      return;
    }

    setLoading(true);
    try {
      const requestData = contactType === 'email' 
        ? { email: contact } 
        : { phone: contact };
      
      const response = await axios.post(`${API}/auth/request-otp`, requestData);
      toast.success('OTP sent successfully!');
      setStep('verify');
    } catch (error) {
      toast.error('Failed to send OTP');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const verifyOTP = async () => {
    if (!otp.trim()) {
      toast.error('Please enter the OTP');
      return;
    }

    setLoading(true);
    try {
      const verifyData = {
        otp,
        ...(contactType === 'email' ? { email: contact } : { phone: contact })
      };
      
      const response = await axios.post(`${API}/auth/verify-otp`, verifyData);
      
      setToken(response.data.access_token);
      toast.success('Successfully signed in!');
      onClose();
    } catch (error) {
      toast.error('Invalid OTP');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Sign In to Clouds Kitchen</DialogTitle>
        </DialogHeader>
        
        {step === 'request' ? (
          <div className="space-y-4">
            <Tabs value={contactType} onValueChange={setContactType}>
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="phone">Phone</TabsTrigger>
                <TabsTrigger value="email">Email</TabsTrigger>
              </TabsList>
            </Tabs>
            
            <div>
              <Label>
                {contactType === 'email' ? 'Email Address' : 'Phone Number'}
              </Label>
              <Input
                type={contactType === 'email' ? 'email' : 'tel'}
                placeholder={contactType === 'email' ? 'Enter your email' : 'Enter your phone number'}
                value={contact}
                onChange={(e) => setContact(e.target.value)}
              />
            </div>
            
            <Button 
              onClick={requestOTP} 
              className="w-full bg-green-600 hover:bg-green-700"
              disabled={loading}
            >
              {loading ? 'Sending...' : 'Send OTP'}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-sm text-gray-600">
              We've sent a verification code to {contact}
            </p>
            
            <div>
              <Label>Verification Code</Label>
              <Input
                type="text"
                placeholder="Enter 6-digit OTP"
                value={otp}
                onChange={(e) => setOTP(e.target.value)}
                maxLength={6}
              />
            </div>
            
            <div className="flex gap-2">
              <Button 
                variant="outline"
                onClick={() => setStep('request')}
                className="flex-1"
              >
                Back
              </Button>
              <Button 
                onClick={verifyOTP}
                className="flex-1 bg-green-600 hover:bg-green-700"
                disabled={loading}
              >
                {loading ? 'Verifying...' : 'Verify OTP'}
              </Button>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}

// Checkout Page Component
function CheckoutPage() {
  const { cart, getCartTotal, user, token } = React.useContext(AppContext);
  const [showAuth, setShowAuth] = useState(!user);
  const [addresses, setAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [newAddress, setNewAddress] = useState({
    street: '',
    city: '',
    state: '',
    pincode: '',
    landmark: ''
  });
  const [loading, setLoading] = useState(false);

  // Redirect to cart if empty
  if (cart.length === 0) {
    return <Navigate to="/cart" replace />;
  }

  // Show auth modal if user not logged in
  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="container mx-auto px-4 py-8">
          <div className="text-center py-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Please sign in to continue</h2>
            <p className="text-gray-600 mb-6">You need to be signed in to place an order</p>
            {showAuth && <AuthModal onClose={() => setShowAuth(false)} />}
          </div>
        </div>
      </div>
    );
  }

  const placeOrder = async () => {
    if (!selectedAddress && !newAddress.street) {
      toast.error('Please provide delivery address');
      return;
    }

    setLoading(true);
    try {
      const orderData = {
        items: cart.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity,
          customizations: item.customizations,
          calculated_price: item.calculated_price
        })),
        delivery_address: selectedAddress || newAddress,
        payment_method: 'cod'
      };

      const response = await axios.post(`${API}/orders`, orderData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      toast.success('Order placed successfully!');
      // Clear cart
      localStorage.removeItem('cart');
      window.location.href = '/profile';
    } catch (error) {
      toast.error('Failed to place order');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Checkout</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Delivery Address</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label>Street Address</Label>
                    <Textarea
                      placeholder="Enter your full address"
                      value={newAddress.street}
                      onChange={(e) => setNewAddress(prev => ({...prev, street: e.target.value}))}
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label>City</Label>
                      <Input
                        placeholder="City"
                        value={newAddress.city}
                        onChange={(e) => setNewAddress(prev => ({...prev, city: e.target.value}))}
                      />
                    </div>
                    <div>
                      <Label>Pincode</Label>
                      <Input
                        placeholder="Pincode"
                        value={newAddress.pincode}
                        onChange={(e) => setNewAddress(prev => ({...prev, pincode: e.target.value}))}
                      />
                    </div>
                  </div>
                  
                  <div>
                    <Label>Landmark (Optional)</Label>
                    <Input
                      placeholder="Nearby landmark"
                      value={newAddress.landmark}
                      onChange={(e) => setNewAddress(prev => ({...prev, landmark: e.target.value}))}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
          
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Order Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {cart.map((item, index) => (
                    <div key={index} className="flex justify-between">
                      <span>{item.product.name} x {item.quantity}</span>
                      <span>₹{item.calculated_price}</span>
                    </div>
                  ))}
                  
                  <div className="border-t pt-3">
                    <div className="flex justify-between font-bold text-lg">
                      <span>Total</span>
                      <span className="text-green-600">₹{getCartTotal()}</span>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6">
                  <Label className="text-sm font-medium">Payment Method</Label>
                  <div className="mt-2 p-3 border rounded-lg bg-green-50">
                    <div className="flex items-center">
                      <span className="font-medium">Cash on Delivery</span>
                      <Badge className="ml-2 bg-green-100 text-green-700">Available</Badge>
                    </div>
                  </div>
                </div>
                
                <Button 
                  onClick={placeOrder}
                  className="w-full mt-6 bg-green-600 hover:bg-green-700"
                  disabled={loading}
                >
                  {loading ? 'Placing Order...' : `Place Order - ₹${getCartTotal()}`}
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

// Profile Page
function ProfilePage() {
  const { user, token, setToken } = React.useContext(AppContext);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user && token) {
      loadOrders();
    }
  }, [user, token]);

  const loadOrders = async () => {
    try {
      const response = await axios.get(`${API}/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(response.data);
    } catch (error) {
      console.error('Failed to load orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    window.location.href = '/';
  };

  if (!user) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
          <Button variant="outline" onClick={logout}>
            Sign Out
          </Button>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Profile Information</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <Label className="text-sm font-medium text-gray-600">Name</Label>
                  <p className="font-medium">{user.name}</p>
                </div>
                {user.email && (
                  <div>
                    <Label className="text-sm font-medium text-gray-600">Email</Label>
                    <p className="font-medium">{user.email}</p>
                  </div>
                )}
                {user.phone && (
                  <div>
                    <Label className="text-sm font-medium text-gray-600">Phone</Label>
                    <p className="font-medium">{user.phone}</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
          
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Order History</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <p>Loading orders...</p>
                ) : orders.length === 0 ? (
                  <p className="text-gray-500">No orders yet</p>
                ) : (
                  <div className="space-y-4">
                    {orders.map(order => (
                      <div key={order.id} className="border rounded-lg p-4">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <h3 className="font-semibold">Order #{order.id.slice(-8)}</h3>
                            <p className="text-sm text-gray-600">
                              {new Date(order.order_date).toLocaleDateString()}
                            </p>
                          </div>
                          <Badge className="bg-green-100 text-green-700">
                            {order.order_status}
                          </Badge>
                        </div>
                        
                        <div className="text-sm space-y-1">
                          <p><strong>Items:</strong> {order.items.length}</p>
                          <p><strong>Total:</strong> ₹{order.total_amount}</p>
                          <p><strong>Payment:</strong> {order.payment_method.toUpperCase()}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

// Footer Component
function Footer() {
  return (
    <footer className="bg-gray-900 text-white py-12 mt-16">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-orange-500 rounded-full flex items-center justify-center">
                <Leaf className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-xl font-bold">Clouds Kitchen</h3>
            </div>
            <p className="text-gray-300 text-sm">
              Bringing you the finest vegetarian and vegan cuisine with authentic flavors and modern presentation.
            </p>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm text-gray-300">
              <li><a href="/" className="hover:text-white">Home</a></li>
              <li><a href="/#menu" className="hover:text-white">Menu</a></li>
              <li><a href="/cart" className="hover:text-white">Cart</a></li>
              <li><a href="/profile" className="hover:text-white">My Account</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Categories</h4>
            <ul className="space-y-2 text-sm text-gray-300">
              <li><span className="hover:text-white">🌱 Vegan Specials</span></li>
              <li><span className="hover:text-white">🥛 Vegetarian Classics</span></li>
              <li><span className="hover:text-white">🎉 Festival Specials</span></li>
              <li><span className="hover:text-white">🥗 Healthy Bowls</span></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Contact Info</h4>
            <ul className="space-y-3 text-sm text-gray-300">
              <li className="flex items-center">
                <Phone className="w-4 h-4 mr-2" />
                +91 98765 43210
              </li>
              <li className="flex items-center">
                <Mail className="w-4 h-4 mr-2" />
                hello@cloudskitchen.com
              </li>
              <li className="flex items-center">
                <MapPin className="w-4 h-4 mr-2" />
                Bangalore, India
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; 2024 Clouds Kitchen. All rights reserved. Made with ❤️ for vegetarian food lovers.</p>
        </div>
      </div>
    </footer>
  );
}

// Admin Components and Routes
function AdminRoutes() {
  return (
    <Routes>
      <Route index element={<AdminLogin />} />
      <Route path="login" element={<AdminLogin />} />
      <Route path="dashboard" element={<AdminDashboard />} />
      <Route path="products" element={<AdminProducts />} />
      <Route path="products/new" element={<AdminProductForm />} />
      <Route path="products/:id/edit" element={<AdminProductForm />} />
      <Route path="orders" element={<AdminOrders />} />
    </Routes>
  );
}

// Admin Context for authentication
const AdminContext = React.createContext();

function AdminLogin() {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post(`${API}/admin/login`, credentials);
      localStorage.setItem('admin_token', response.data.access_token);
      localStorage.setItem('admin_username', response.data.username);
      
      toast.success('Welcome to Admin Dashboard!');
      window.location.href = '/admin/dashboard';
    } catch (error) {
      toast.error('Invalid admin credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-orange-500 rounded-full flex items-center justify-center">
              <Leaf className="w-8 h-8 text-white" />
            </div>
          </div>
          <CardTitle className="text-2xl">Admin Login</CardTitle>
          <p className="text-gray-600">Access Clouds Kitchen Admin Dashboard</p>
        </CardHeader>
        
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                placeholder="Enter username"
                value={credentials.username}
                onChange={(e) => setCredentials(prev => ({...prev, username: e.target.value}))}
                required
              />
            </div>
            
            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter password"
                value={credentials.password}
                onChange={(e) => setCredentials(prev => ({...prev, password: e.target.value}))}
                required
              />
            </div>
            
            <Button 
              type="submit" 
              className="w-full bg-blue-600 hover:bg-blue-700"
              disabled={loading}
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>
          
          <div className="mt-6 text-center text-sm text-gray-500">
            <p>Demo Credentials:</p>
            <p><strong>Username:</strong> admin | <strong>Password:</strong> cloudskitchen123</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Admin Dashboard Component
function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/admin/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
      if (error.response?.status === 401) {
        window.location.href = '/admin/login';
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <AdminLayout><div className="p-8 text-center">Loading dashboard...</div></AdminLayout>;
  }

  return (
    <AdminLayout>
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <Badge className="bg-green-100 text-green-800">
            Welcome, {localStorage.getItem('admin_username')}
          </Badge>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <ShoppingCart className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Total Products</p>
                  <p className="text-2xl font-bold">{stats?.total_products || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <User className="w-6 h-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Total Users</p>
                  <p className="text-2xl font-bold">{stats?.total_users || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <ShoppingCart className="w-6 h-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Total Orders</p>
                  <p className="text-2xl font-bold">{stats?.total_orders || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-red-100 rounded-lg">
                  <Star className="w-6 h-6 text-red-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Low Stock Items</p>
                  <p className="text-2xl font-bold">{stats?.low_stock_products || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Button 
                  onClick={() => window.location.href = '/admin/products/new'}
                  className="w-full bg-green-600 hover:bg-green-700"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add New Product
                </Button>
                
                <Button 
                  onClick={() => window.location.href = '/admin/products'}
                  variant="outline"
                  className="w-full"
                >
                  Manage Products
                </Button>
                
                <Button 
                  onClick={() => window.location.href = '/admin/orders'}
                  variant="outline"
                  className="w-full"
                >
                  View Orders
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Low Stock Items */}
          {stats?.low_stock_items && stats.low_stock_items.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-red-600">Low Stock Alert</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {stats.low_stock_items.slice(0, 5).map(item => (
                    <div key={item.id} className="flex justify-between items-center p-2 bg-red-50 rounded">
                      <div>
                        <p className="font-medium text-sm">{item.name}</p>
                        <p className="text-xs text-gray-600">{item.category}</p>
                      </div>
                      <Badge variant="destructive">
                        {item.stock_quantity} left
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </AdminLayout>
  );
}

// Admin Layout Component
function AdminLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const logout = () => {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_username');
    window.location.href = '/admin/login';
  };

  const menuItems = [
    { name: 'Dashboard', path: '/admin/dashboard', icon: Star },
    { name: 'Products', path: '/admin/products', icon: ShoppingCart },
    { name: 'Orders', path: '/admin/orders', icon: User },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6 border-b">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-orange-500 rounded-full flex items-center justify-center">
              <Leaf className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="font-bold text-gray-900">Admin Panel</h2>
              <p className="text-sm text-gray-600">Clouds Kitchen</p>
            </div>
          </div>
        </div>

        <nav className="p-4">
          <ul className="space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              return (
                <li key={item.name}>
                  <a
                    href={item.path}
                    className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <Icon className="w-5 h-5 text-gray-600" />
                    <span className="text-gray-700">{item.name}</span>
                  </a>
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="absolute bottom-4 left-4 right-4">
          <Button 
            onClick={logout}
            variant="outline" 
            className="w-full"
          >
            Logout
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        <header className="bg-white shadow-sm border-b px-6 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-xl font-semibold text-gray-900">Admin Dashboard</h1>
            <div className="text-sm text-gray-600">
              Welcome, {localStorage.getItem('admin_username')}
            </div>
          </div>
        </header>
        
        <main>
          {children}
        </main>
      </div>
    </div>
  );
}

// Admin Products Component
function AdminProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/admin/products`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProducts(response.data);
    } catch (error) {
      console.error('Failed to load products:', error);
      if (error.response?.status === 401) {
        window.location.href = '/admin/login';
      }
    } finally {
      setLoading(false);
    }
  };

  const toggleProductStatus = async (productId) => {
    try {
      const token = localStorage.getItem('admin_token');
      await axios.post(`${API}/admin/products/${productId}/toggle-status`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await loadProducts(); // Refresh the list
      toast.success('Product status updated');
    } catch (error) {
      toast.error('Failed to update product status');
    }
  };

  const deleteProduct = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;
    
    try {
      const token = localStorage.getItem('admin_token');
      await axios.delete(`${API}/admin/products/${productId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await loadProducts();
      toast.success('Product deleted successfully');
    } catch (error) {
      toast.error('Failed to delete product');
    }
  };

  const filteredProducts = products.filter(product => {
    if (filter === 'all') return true;
    if (filter === 'active') return product.is_active;
    if (filter === 'inactive') return !product.is_active;
    if (filter === 'low-stock') return product.stock_quantity <= product.min_stock_level;
    return product.category === filter;
  });

  return (
    <AdminLayout>
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Product Management</h1>
          <Button 
            onClick={() => window.location.href = '/admin/products/new'}
            className="bg-green-600 hover:bg-green-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Product
          </Button>
        </div>

        {/* Filters */}
        <div className="mb-6">
          <div className="flex flex-wrap gap-2">
            {['all', 'active', 'inactive', 'low-stock', 'vegan', 'vegetarian'].map(filterOption => (
              <Button
                key={filterOption}
                variant={filter === filterOption ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilter(filterOption)}
                className="capitalize"
              >
                {filterOption.replace('-', ' ')}
                {filterOption === filter && (
                  <Badge className="ml-2 bg-white text-gray-800">
                    {filteredProducts.length}
                  </Badge>
                )}
              </Button>
            ))}
          </div>
        </div>

        {/* Products Table */}
        {loading ? (
          <div className="text-center py-8">Loading products...</div>
        ) : (
          <Card>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b">
                  <tr className="text-left">
                    <th className="p-4">Product</th>
                    <th className="p-4">Category</th>
                    <th className="p-4">Price</th>
                    <th className="p-4">Stock</th>
                    <th className="p-4">Status</th>
                    <th className="p-4">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProducts.map(product => (
                    <tr key={product.id} className="border-b hover:bg-gray-50">
                      <td className="p-4">
                        <div className="flex items-center space-x-3">
                          <img 
                            src={product.images[0]} 
                            alt={product.name}
                            className="w-12 h-12 rounded-lg object-cover"
                          />
                          <div>
                            <p className="font-medium">{product.name}</p>
                            <p className="text-sm text-gray-600 capitalize">
                              {product.subcategory?.replace('-', ' ')}
                            </p>
                          </div>
                        </div>
                      </td>
                      <td className="p-4">
                        <Badge className={
                          product.category === 'vegan' 
                            ? 'bg-green-100 text-green-800'
                            : 'bg-orange-100 text-orange-800'
                        }>
                          {product.category}
                        </Badge>
                      </td>
                      <td className="p-4">₹{product.base_price}</td>
                      <td className="p-4">
                        <div className="flex items-center space-x-2">
                          <span>{product.stock_quantity}</span>
                          {product.stock_quantity <= product.min_stock_level && (
                            <Badge variant="destructive">Low</Badge>
                          )}
                        </div>
                      </td>
                      <td className="p-4">
                        <Badge className={
                          product.is_active 
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }>
                          {product.is_active ? 'Active' : 'Inactive'}
                        </Badge>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => window.location.href = `/admin/products/${product.id}/edit`}
                          >
                            Edit
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => toggleProductStatus(product.id)}
                          >
                            {product.is_active ? 'Deactivate' : 'Activate'}
                          </Button>
                          <Button
                            size="sm"
                            variant="destructive"
                            onClick={() => deleteProduct(product.id)}
                          >
                            Delete
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        )}
      </div>
    </AdminLayout>
  );
}

// Admin Product Form Component
function AdminProductForm() {
  const [product, setProduct] = useState({
    name: '',
    description: '',
    images: [''],
    category: 'vegetarian',
    subcategory: 'north-indian',
    base_price: '',
    stock_quantity: 100,
    min_stock_level: 10,
    preparation_time: 20,
    tags: [],
    customization_options: {}
  });
  const [loading, setLoading] = useState(false);
  const [newTag, setNewTag] = useState('');

  const subcategories = {
    'north-indian': 'North Indian',
    'south-indian': 'South Indian',
    'street-food': 'Street Food',
    'sweets': 'Sweets',
    'beverages': 'Beverages',
    'snacks': 'Snacks',
    'international': 'International'
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const token = localStorage.getItem('admin_token');
      const productData = {
        ...product,
        base_price: parseFloat(product.base_price),
        stock_quantity: parseInt(product.stock_quantity),
        min_stock_level: parseInt(product.min_stock_level),
        preparation_time: parseInt(product.preparation_time)
      };

      await axios.post(`${API}/admin/products`, productData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      toast.success('Product created successfully!');
      window.location.href = '/admin/products';
    } catch (error) {
      toast.error('Failed to create product');
    } finally {
      setLoading(false);
    }
  };

  const addTag = () => {
    if (newTag.trim() && !product.tags.includes(newTag.trim())) {
      setProduct(prev => ({
        ...prev,
        tags: [...prev.tags, newTag.trim()]
      }));
      setNewTag('');
    }
  };

  const removeTag = (tagToRemove) => {
    setProduct(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove)
    }));
  };

  return (
    <AdminLayout>
      <div className="p-6">
        <div className="flex items-center mb-6">
          <Button 
            variant="outline" 
            onClick={() => window.location.href = '/admin/products'}
            className="mr-4"
          >
            ← Back
          </Button>
          <h1 className="text-2xl font-bold text-gray-900">Add New Product</h1>
        </div>

        <Card>
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Basic Information */}
                <div className="space-y-4">
                  <div>
                    <Label>Product Name</Label>
                    <Input
                      value={product.name}
                      onChange={(e) => setProduct(prev => ({...prev, name: e.target.value}))}
                      placeholder="Enter product name"
                      required
                    />
                  </div>

                  <div>
                    <Label>Description</Label>
                    <Textarea
                      value={product.description}
                      onChange={(e) => setProduct(prev => ({...prev, description: e.target.value}))}
                      placeholder="Enter product description"
                      rows={3}
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label>Category</Label>
                      <Select 
                        value={product.category}
                        onValueChange={(value) => setProduct(prev => ({...prev, category: value}))}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="vegetarian">Vegetarian</SelectItem>
                          <SelectItem value="vegan">Vegan</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label>Subcategory</Label>
                      <Select 
                        value={product.subcategory}
                        onValueChange={(value) => setProduct(prev => ({...prev, subcategory: value}))}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {Object.entries(subcategories).map(([key, label]) => (
                            <SelectItem key={key} value={key}>{label}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label>Image URL</Label>
                    <Input
                      value={product.images[0]}
                      onChange={(e) => setProduct(prev => ({
                        ...prev, 
                        images: [e.target.value]
                      }))}
                      placeholder="Enter image URL"
                      required
                    />
                  </div>
                </div>

                {/* Pricing & Inventory */}
                <div className="space-y-4">
                  <div>
                    <Label>Base Price (₹)</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={product.base_price}
                      onChange={(e) => setProduct(prev => ({...prev, base_price: e.target.value}))}
                      placeholder="0.00"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label>Stock Quantity</Label>
                      <Input
                        type="number"
                        value={product.stock_quantity}
                        onChange={(e) => setProduct(prev => ({...prev, stock_quantity: e.target.value}))}
                        required
                      />
                    </div>

                    <div>
                      <Label>Min Stock Level</Label>
                      <Input
                        type="number"
                        value={product.min_stock_level}
                        onChange={(e) => setProduct(prev => ({...prev, min_stock_level: e.target.value}))}
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <Label>Preparation Time (minutes)</Label>
                    <Input
                      type="number"
                      value={product.preparation_time}
                      onChange={(e) => setProduct(prev => ({...prev, preparation_time: e.target.value}))}
                      required
                    />
                  </div>

                  {/* Tags */}
                  <div>
                    <Label>Tags</Label>
                    <div className="flex space-x-2 mb-2">
                      <Input
                        value={newTag}
                        onChange={(e) => setNewTag(e.target.value)}
                        placeholder="Add a tag"
                        onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
                      />
                      <Button type="button" onClick={addTag}>Add</Button>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {product.tags.map(tag => (
                        <Badge key={tag} variant="secondary" className="cursor-pointer">
                          {tag}
                          <button 
                            type="button"
                            onClick={() => removeTag(tag)}
                            className="ml-1 text-red-500 hover:text-red-700"
                          >
                            ×
                          </button>
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-end space-x-4">
                <Button 
                  type="button" 
                  variant="outline"
                  onClick={() => window.location.href = '/admin/products'}
                >
                  Cancel
                </Button>
                <Button 
                  type="submit" 
                  className="bg-green-600 hover:bg-green-700"
                  disabled={loading}
                >
                  {loading ? 'Creating...' : 'Create Product'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  );
}

// Admin Orders Component
function AdminOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await axios.get(`${API}/admin/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(response.data);
    } catch (error) {
      console.error('Failed to load orders:', error);
      if (error.response?.status === 401) {
        window.location.href = '/admin/login';
      }
    } finally {
      setLoading(false);
    }
  };

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      const token = localStorage.getItem('admin_token');
      await axios.put(`${API}/admin/orders/${orderId}/status`, 
        { order_status: newStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      await loadOrders();
      toast.success('Order status updated');
    } catch (error) {
      toast.error('Failed to update order status');
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      placed: 'bg-blue-100 text-blue-800',
      confirmed: 'bg-yellow-100 text-yellow-800',
      preparing: 'bg-orange-100 text-orange-800',
      ready: 'bg-purple-100 text-purple-800',
      dispatched: 'bg-indigo-100 text-indigo-800',
      delivered: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <AdminLayout>
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Order Management</h1>
        </div>

        {loading ? (
          <div className="text-center py-8">Loading orders...</div>
        ) : (
          <Card>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b">
                  <tr className="text-left">
                    <th className="p-4">Order ID</th>
                    <th className="p-4">Customer</th>
                    <th className="p-4">Items</th>
                    <th className="p-4">Total</th>
                    <th className="p-4">Status</th>
                    <th className="p-4">Date</th>
                    <th className="p-4">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map(order => (
                    <tr key={order.id} className="border-b hover:bg-gray-50">
                      <td className="p-4 font-mono text-sm">
                        #{order.id.slice(-8)}
                      </td>
                      <td className="p-4">{order.user_id.slice(-8)}</td>
                      <td className="p-4">{order.items.length} items</td>
                      <td className="p-4 font-medium">₹{order.total_amount}</td>
                      <td className="p-4">
                        <Badge className={getStatusColor(order.order_status)}>
                          {order.order_status}
                        </Badge>
                      </td>
                      <td className="p-4 text-sm text-gray-600">
                        {new Date(order.order_date).toLocaleDateString()}
                      </td>
                      <td className="p-4">
                        <Select 
                          value={order.order_status}
                          onValueChange={(value) => updateOrderStatus(order.id, value)}
                        >
                          <SelectTrigger className="w-32">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="placed">Placed</SelectItem>
                            <SelectItem value="confirmed">Confirmed</SelectItem>
                            <SelectItem value="preparing">Preparing</SelectItem>
                            <SelectItem value="ready">Ready</SelectItem>
                            <SelectItem value="dispatched">Dispatched</SelectItem>
                            <SelectItem value="delivered">Delivered</SelectItem>
                            <SelectItem value="cancelled">Cancelled</SelectItem>
                          </SelectContent>
                        </Select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        )}
      </div>
    </AdminLayout>
  );
}

export default App;