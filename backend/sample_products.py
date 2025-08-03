"""
Expanded product catalog for Clouds Kitchen
40 authentic Indian vegetarian and vegan dishes
"""

# Complete product catalog with all fields
EXPANDED_PRODUCT_CATALOG = [
    # NORTH INDIAN DISHES (8 products)
    {
        "name": "Dal Makhani",
        "description": "Rich and creamy black lentils slow-cooked with butter, cream, and aromatic spices",
        "images": ["https://images.unsplash.com/photo-1546833999-b9f581a1996d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxkYWwlMjBtYWtoYW5pfGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "north-indian",
        "base_price": 249.0,
        "stock_quantity": 50,
        "min_stock_level": 5,
        "preparation_time": 25,
        "tags": ["dal", "lentils", "creamy", "north-indian", "punjabi"],
        "customization_options": {
            "spice_level": {
                "enabled": True,
                "options": [
                    {"name": "Mild", "price_modifier": 0},
                    {"name": "Medium", "price_modifier": 0},
                    {"name": "Spicy", "price_modifier": 0}
                ]
            },
            "serving_size": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Large", "price_modifier": 50}
                ]
            }
        }
    },
    {
        "name": "Paneer Butter Masala",
        "description": "Tender cottage cheese cubes in rich tomato and cashew gravy with aromatic spices",
        "images": ["https://images.unsplash.com/photo-1631452180539-96aca7d48617?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxwYW5lZXIlMjBidXR0ZXIlMjBtYXNhbGF8ZW58MHx8fHwxNzU0MjExMTI3fDA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "north-indian",
        "base_price": 299.0,
        "stock_quantity": 40,
        "min_stock_level": 8,
        "preparation_time": 20,
        "tags": ["paneer", "cottage cheese", "tomato", "north-indian", "punjabi"],
        "customization_options": {
            "spice_level": {
                "enabled": True,
                "options": [
                    {"name": "Mild", "price_modifier": 0},
                    {"name": "Medium", "price_modifier": 0},
                    {"name": "Spicy", "price_modifier": 0}
                ]
            },
            "paneer_quantity": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Paneer", "price_modifier": 40}
                ]
            }
        }
    },
    {
        "name": "Chole Bhature",
        "description": "Spicy chickpea curry served with fluffy deep-fried bread, a classic Punjabi favorite",
        "images": ["https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxjaG9sZSUyMGJoYXR1cmV8ZW58MHx8fHwxNzU0MjExMTI3fDA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "north-indian",
        "base_price": 199.0,
        "stock_quantity": 60,
        "min_stock_level": 10,
        "preparation_time": 15,
        "tags": ["chole", "chickpeas", "bhature", "punjabi", "bread"],
        "customization_options": {
            "bhature_count": {
                "enabled": True,
                "options": [
                    {"name": "1 Bhature", "price_modifier": 0},
                    {"name": "2 Bhature", "price_modifier": 30},
                    {"name": "3 Bhature", "price_modifier": 50}
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
        "name": "Rajma Chawal",
        "description": "Hearty kidney bean curry served with steamed basmati rice, comfort food at its best",
        "images": ["https://images.unsplash.com/photo-1585937421612-70a008356fbe?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxyYWptYSUyMGNoYXdhbHxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "north-indian",
        "base_price": 179.0,
        "stock_quantity": 70,
        "min_stock_level": 12,
        "preparation_time": 18,
        "tags": ["rajma", "kidney beans", "rice", "comfort food", "punjabi"],
        "customization_options": {
            "rice_type": {
                "enabled": True,
                "options": [
                    {"name": "Steamed Rice", "price_modifier": 0},
                    {"name": "Jeera Rice", "price_modifier": 20},
                    {"name": "Brown Rice", "price_modifier": 15}
                ]
            }
        }
    },
    {
        "name": "Aloo Gobi",
        "description": "Dry curry of cauliflower and potatoes cooked with turmeric and aromatic spices",
        "images": ["https://images.unsplash.com/photo-1565557623262-b51c2513a641?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxhbG9vJTIwZ29iaXxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "north-indian",
        "base_price": 149.0,
        "stock_quantity": 80,
        "min_stock_level": 15,
        "preparation_time": 22,
        "tags": ["aloo", "gobi", "cauliflower", "potato", "vegan", "dry curry"],
        "customization_options": {
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
        "name": "Palak Paneer",
        "description": "Fresh cottage cheese cubes in creamy spinach gravy, packed with iron and flavor",
        "images": ["https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxwYWxhayUyMHBhbmVlcnxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "north-indian",
        "base_price": 279.0,
        "stock_quantity": 45,
        "min_stock_level": 8,
        "preparation_time": 25,
        "tags": ["palak", "spinach", "paneer", "healthy", "green"],
        "customization_options": {
            "paneer_quantity": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Paneer", "price_modifier": 40}
                ]
            },
            "cream_level": {
                "enabled": True,
                "options": [
                    {"name": "Light", "price_modifier": 0},
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Creamy", "price_modifier": 20}
                ]
            }
        }
    },
    {
        "name": "Kadhi Pakora",
        "description": "Tangy yogurt-based curry with gram flour fritters, a comfort food classic",
        "images": ["https://images.unsplash.com/photo-1596797038530-2c107229654b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxrYWRoaSUyMHBha29yYXxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "north-indian",
        "base_price": 189.0,
        "stock_quantity": 55,
        "min_stock_level": 10,
        "preparation_time": 30,
        "tags": ["kadhi", "pakora", "yogurt", "tangy", "comfort food"],
        "customization_options": {
            "pakora_quantity": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Pakoras", "price_modifier": 30}
                ]
            }
        }
    },
    {
        "name": "Matar Paneer",
        "description": "Cottage cheese and green peas in spiced tomato gravy, a homestyle favorite",
        "images": ["https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxtYXRhciUyMHBhbmVlcnxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "north-indian",
        "base_price": 259.0,
        "stock_quantity": 50,
        "min_stock_level": 8,
        "preparation_time": 20,
        "tags": ["matar", "peas", "paneer", "homestyle", "tomato gravy"],
        "customization_options": {
            "peas_quantity": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Peas", "price_modifier": 20}
                ]
            }
        }
    },

    # SOUTH INDIAN DISHES (8 products)
    {
        "name": "Masala Dosa",
        "description": "Crispy rice and lentil crepe filled with spiced potato mixture, served with chutneys",
        "images": ["https://images.unsplash.com/photo-1554047071-9dc8c0f7b735?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxtYXNhbGElMjBkb3NhfGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "south-indian",
        "base_price": 129.0,
        "stock_quantity": 100,
        "min_stock_level": 20,
        "preparation_time": 15,
        "tags": ["dosa", "masala", "crispy", "south-indian", "fermented"],
        "customization_options": {
            "crispiness": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Crispy", "price_modifier": 10},
                    {"name": "Soft", "price_modifier": 0}
                ]
            },
            "chutney": {
                "enabled": True,
                "options": [
                    {"name": "Coconut", "price_modifier": 0},
                    {"name": "Tomato", "price_modifier": 0},
                    {"name": "Both", "price_modifier": 15}
                ]
            }
        }
    },
    {
        "name": "Idli Sambar",
        "description": "Steamed rice cakes served with lentil soup and coconut chutney, healthy breakfast",
        "images": ["https://images.unsplash.com/photo-1589301760014-d929f3979dbc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxpZGxpJTIwc2FtYmFyfGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "south-indian",
        "base_price": 99.0,
        "stock_quantity": 120,
        "min_stock_level": 25,
        "preparation_time": 10,
        "tags": ["idli", "sambar", "healthy", "steamed", "fermented"],
        "customization_options": {
            "idli_count": {
                "enabled": True,
                "options": [
                    {"name": "3 Idli", "price_modifier": 0},
                    {"name": "4 Idli", "price_modifier": 20},
                    {"name": "5 Idli", "price_modifier": 35}
                ]
            }
        }
    },
    {
        "name": "Medu Vada",
        "description": "Crispy deep-fried lentil donuts served with sambar and chutney, crunchy delight",
        "images": ["https://images.unsplash.com/photo-1606491956689-2ea866880c84?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxtZWR1JTIwdmFkYXxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "south-indian",
        "base_price": 89.0,
        "stock_quantity": 90,
        "min_stock_level": 18,
        "preparation_time": 12,
        "tags": ["vada", "crispy", "lentil", "fried", "donut"],
        "customization_options": {
            "vada_count": {
                "enabled": True,
                "options": [
                    {"name": "2 Vada", "price_modifier": 0},
                    {"name": "3 Vada", "price_modifier": 25},
                    {"name": "4 Vada", "price_modifier": 45}
                ]
            }
        }
    },
    {
        "name": "Rava Upma",
        "description": "Savory semolina porridge cooked with vegetables and South Indian spices",
        "images": ["https://images.unsplash.com/photo-1546833999-b9f581a1996d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHxyYXZhJTIwdXBtYXxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "south-indian",
        "base_price": 79.0,
        "stock_quantity": 110,
        "min_stock_level": 22,
        "preparation_time": 15,
        "tags": ["upma", "semolina", "vegetables", "breakfast", "healthy"],
        "customization_options": {
            "vegetables": {
                "enabled": True,
                "options": [
                    {"name": "Regular Mix", "price_modifier": 0},
                    {"name": "Extra Vegetables", "price_modifier": 20},
                    {"name": "Peas Special", "price_modifier": 15}
                ]
            }
        }
    },
    {
        "name": "Coconut Rice",
        "description": "Fragrant rice cooked with coconut, curry leaves, and traditional South Indian spices",
        "images": ["https://images.unsplash.com/photo-1563379091339-03246963d396?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxjb2NvbnV0JTIwcmljZXxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "south-indian",
        "base_price": 149.0,
        "stock_quantity": 80,
        "min_stock_level": 15,
        "preparation_time": 20,
        "tags": ["coconut", "rice", "fragrant", "curry leaves", "traditional"],
        "customization_options": {
            "coconut_level": {
                "enabled": True,
                "options": [
                    {"name": "Light", "price_modifier": 0},
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Rich", "price_modifier": 20}
                ]
            }
        }
    },
    {
        "name": "Rasam Rice",
        "description": "Tangy tamarind-based soup with rice, tempered with mustard seeds and curry leaves",
        "images": ["https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHxyYXNhbSUyMHJpY2V8ZW58MHx8fHwxNzU0MjExMTI3fDA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "south-indian",
        "base_price": 119.0,
        "stock_quantity": 95,
        "min_stock_level": 18,
        "preparation_time": 15,
        "tags": ["rasam", "tangy", "tamarind", "soup", "digestive"],
        "customization_options": {
            "tanginess": {
                "enabled": True,
                "options": [
                    {"name": "Mild", "price_modifier": 0},
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Tangy", "price_modifier": 10}
                ]
            }
        }
    },
    {
        "name": "Uttapam",
        "description": "Thick pancake made from fermented rice and lentil batter with vegetable toppings",
        "images": ["https://images.unsplash.com/photo-1589301760014-d929f3979dbc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwzfHx1dHRhcGFtfGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "south-indian",
        "base_price": 139.0,
        "stock_quantity": 75,
        "min_stock_level": 15,
        "preparation_time": 18,
        "tags": ["uttapam", "pancake", "fermented", "vegetables", "thick"],
        "customization_options": {
            "toppings": {
                "enabled": True,
                "options": [
                    {"name": "Onion", "price_modifier": 0},
                    {"name": "Tomato Onion", "price_modifier": 15},
                    {"name": "Mixed Vegetable", "price_modifier": 25}
                ]
            }
        }
    },
    {
        "name": "Lemon Rice",
        "description": "Aromatic rice tempered with mustard seeds, curry leaves, and fresh lemon juice",
        "images": ["https://images.unsplash.com/photo-1563379091339-03246963d396?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHw0fHxsZW1vbiUyMHJpY2V8ZW58MHx8fHwxNzU0MjExMTI3fDA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "south-indian",
        "base_price": 109.0,
        "stock_quantity": 85,
        "min_stock_level": 17,
        "preparation_time": 12,
        "tags": ["lemon", "rice", "tangy", "refreshing", "light"],
        "customization_options": {
            "lemon_intensity": {
                "enabled": True,
                "options": [
                    {"name": "Mild", "price_modifier": 0},
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Lemony", "price_modifier": 10}
                ]
            }
        }
    },

    # STREET FOOD (6 products)
    {
        "name": "Pav Bhaji",
        "description": "Spicy mixed vegetable curry served with buttered and toasted bread rolls",
        "images": ["https://images.unsplash.com/photo-1626074353765-517a681e40be?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxwYXYlMjBiaGFqaXxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "street-food",
        "base_price": 149.0,
        "stock_quantity": 90,
        "min_stock_level": 18,
        "preparation_time": 15,
        "tags": ["pav", "bhaji", "street food", "mumbai", "spicy"],
        "customization_options": {
            "butter_level": {
                "enabled": True,
                "options": [
                    {"name": "Light Butter", "price_modifier": 0},
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Butter", "price_modifier": 15}
                ]
            },
            "pav_count": {
                "enabled": True,
                "options": [
                    {"name": "2 Pav", "price_modifier": 0},
                    {"name": "3 Pav", "price_modifier": 20},
                    {"name": "4 Pav", "price_modifier": 35}
                ]
            }
        }
    },
    {
        "name": "Bhel Puri",
        "description": "Crunchy mixture of puffed rice, sev, vegetables, and tangy chutneys",
        "images": ["https://images.unsplash.com/photo-1606491956689-2ea866880c84?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHxiaGVsJTIwcHVyaXxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "street-food",
        "base_price": 79.0,
        "stock_quantity": 150,
        "min_stock_level": 30,
        "preparation_time": 8,
        "tags": ["bhel", "puffed rice", "chaat", "crunchy", "tangy"],
        "customization_options": {
            "spice_level": {
                "enabled": True,
                "options": [
                    {"name": "Mild", "price_modifier": 0},
                    {"name": "Medium", "price_modifier": 0},
                    {"name": "Spicy", "price_modifier": 0}
                ]
            },
            "extra_toppings": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Sev", "price_modifier": 10},
                    {"name": "Extra Vegetables", "price_modifier": 15}
                ]
            }
        }
    },
    {
        "name": "Dhokla",
        "description": "Steamed fermented chickpea flour cake, light and spongy Gujarati delicacy",
        "images": ["https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwzfHxkaG9rbGF8ZW58MHx8fHwxNzU0MjExMTI3fDA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "street-food",
        "base_price": 99.0,
        "stock_quantity": 80,
        "min_stock_level": 16,
        "preparation_time": 12,
        "tags": ["dhokla", "steamed", "gujarati", "spongy", "healthy"],
        "customization_options": {
            "piece_count": {
                "enabled": True,
                "options": [
                    {"name": "4 Pieces", "price_modifier": 0},
                    {"name": "6 Pieces", "price_modifier": 25},
                    {"name": "8 Pieces", "price_modifier": 40}
                ]
            }
        }
    },
    {
        "name": "Vada Pav",
        "description": "Deep-fried potato dumpling in a bread bun, Mumbai's favorite street food",
        "images": ["https://images.unsplash.com/photo-1626074353765-517a681e40be?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHw0fHx2YWRhJTIwcGF2fGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "street-food",
        "base_price": 45.0,
        "stock_quantity": 200,
        "min_stock_level": 40,
        "preparation_time": 10,
        "tags": ["vada pav", "mumbai", "street food", "potato", "fried"],
        "customization_options": {
            "chutney": {
                "enabled": True,
                "options": [
                    {"name": "Green Chutney", "price_modifier": 0},
                    {"name": "Tamarind Chutney", "price_modifier": 0},
                    {"name": "Both", "price_modifier": 5}
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
        "name": "Dahi Puri",
        "description": "Crispy puris filled with yogurt, chutneys, and spices, a refreshing chaat",
        "images": ["https://images.unsplash.com/photo-1606491956689-2ea866880c84?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHw1fHxkYWhpJTIwcHVyaXxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "street-food",
        "base_price": 89.0,
        "stock_quantity": 120,
        "min_stock_level": 24,
        "preparation_time": 8,
        "tags": ["dahi puri", "chaat", "yogurt", "crispy", "refreshing"],
        "customization_options": {
            "yogurt_level": {
                "enabled": True,
                "options": [
                    {"name": "Light", "price_modifier": 0},
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Creamy", "price_modifier": 10}
                ]
            }
        }
    },
    {
        "name": "Aloo Tikki Chaat",
        "description": "Crispy potato patties topped with yogurt, chutneys, and fresh vegetables",
        "images": ["https://images.unsplash.com/photo-1565557623262-b51c2513a641?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHw2fHxhbG9vJTIwdGlra2klMjBjaGFhdHxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "street-food",
        "base_price": 109.0,
        "stock_quantity": 90,
        "min_stock_level": 18,
        "preparation_time": 12,
        "tags": ["aloo tikki", "chaat", "potato", "crispy", "toppings"],
        "customization_options": {
            "tikki_count": {
                "enabled": True,
                "options": [
                    {"name": "2 Tikki", "price_modifier": 0},
                    {"name": "3 Tikki", "price_modifier": 30},
                    {"name": "4 Tikki", "price_modifier": 50}
                ]
            }
        }
    },

    # SWEETS (4 products)
    {
        "name": "Gulab Jamun",
        "description": "Soft milk dumplings soaked in rose-flavored sugar syrup, a classic Indian dessert",
        "images": ["https://images.unsplash.com/photo-1571167562160-ca4755e8a0c8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxndWxhYiUyMGphbXVufGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "sweets",
        "base_price": 129.0,
        "stock_quantity": 60,
        "min_stock_level": 12,
        "preparation_time": 5,
        "tags": ["gulab jamun", "sweet", "dessert", "milk", "syrup"],
        "customization_options": {
            "piece_count": {
                "enabled": True,
                "options": [
                    {"name": "2 Pieces", "price_modifier": 0},
                    {"name": "4 Pieces", "price_modifier": 50},
                    {"name": "6 Pieces", "price_modifier": 90}
                ]
            },
            "temperature": {
                "enabled": True,
                "options": [
                    {"name": "Room Temperature", "price_modifier": 0},
                    {"name": "Warm", "price_modifier": 0}
                ]
            }
        }
    },
    {
        "name": "Rice Kheer",
        "description": "Creamy rice pudding cooked in milk with cardamom, nuts, and saffron",
        "images": ["https://images.unsplash.com/photo-1571167562160-ca4755e8a0c8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHxyaWNlJTIwa2hlZXJ8ZW58MHx8fHwxNzU0MjExMTI3fDA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "sweets",
        "base_price": 99.0,
        "stock_quantity": 70,
        "min_stock_level": 14,
        "preparation_time": 8,
        "tags": ["kheer", "pudding", "rice", "milk", "cardamom", "nuts"],
        "customization_options": {
            "nuts": {
                "enabled": True,
                "options": [
                    {"name": "Regular Nuts", "price_modifier": 0},
                    {"name": "Extra Nuts", "price_modifier": 20},
                    {"name": "Premium Nuts", "price_modifier": 35}
                ]
            }
        }
    },
    {
        "name": "Gajar Halwa",
        "description": "Rich carrot pudding cooked in milk and ghee, garnished with nuts",
        "images": ["https://images.unsplash.com/photo-1571167562160-ca4755e8a0c8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwzfHxnYWphciUyMGhhbHdhfGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "sweets",
        "base_price": 149.0,
        "stock_quantity": 50,
        "min_stock_level": 10,
        "preparation_time": 10,
        "tags": ["gajar halwa", "carrot", "halwa", "rich", "nuts"],
        "customization_options": {
            "richness": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Rich", "price_modifier": 30}
                ]
            },
            "serving_style": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "With Ice Cream", "price_modifier": 40}
                ]
            }
        }
    },
    {
        "name": "Ras Malai",
        "description": "Soft cottage cheese dumplings in sweet, thickened milk with pistachios",
        "images": ["https://images.unsplash.com/photo-1571167562160-ca4755e8a0c8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHw0fHxyYXMlMjBtYWxhaXxlbnwwfHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "sweets",
        "base_price": 179.0,
        "stock_quantity": 40,
        "min_stock_level": 8,
        "preparation_time": 5,
        "tags": ["ras malai", "cottage cheese", "milk", "pistachios", "soft"],
        "customization_options": {
            "piece_count": {
                "enabled": True,
                "options": [
                    {"name": "2 Pieces", "price_modifier": 0},
                    {"name": "3 Pieces", "price_modifier": 40},
                    {"name": "4 Pieces", "price_modifier": 70}
                ]
            }
        }
    },

    # BEVERAGES (3 products)
    {
        "name": "Sweet Lassi",
        "description": "Refreshing yogurt-based drink blended with sugar and cardamom",
        "images": ["https://images.unsplash.com/photo-1570197788417-0e82375c9371?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxzd2VldCUyMGxhc3NpfGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "beverages",
        "base_price": 69.0,
        "stock_quantity": 150,
        "min_stock_level": 30,
        "preparation_time": 5,
        "tags": ["lassi", "yogurt", "sweet", "refreshing", "cardamom"],
        "customization_options": {
            "size": {
                "enabled": True,
                "options": [
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Large", "price_modifier": 20}
                ]
            },
            "flavor": {
                "enabled": True,
                "options": [
                    {"name": "Plain Sweet", "price_modifier": 0},
                    {"name": "Rose", "price_modifier": 10},
                    {"name": "Saffron", "price_modifier": 15}
                ]
            }
        }
    },
    {
        "name": "Fresh Lime Water",
        "description": "Zesty lime juice with mint leaves, salt, and sugar - perfect thirst quencher",
        "images": ["https://images.unsplash.com/photo-1570197788417-0e82375c9371?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHxsaW1lJTIwd2F0ZXJ8ZW58MHx8fHwxNzU0MjExMTI3fDA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "beverages",
        "base_price": 49.0,
        "stock_quantity": 200,
        "min_stock_level": 40,
        "preparation_time": 3,
        "tags": ["lime", "mint", "refreshing", "zesty", "natural"],
        "customization_options": {
            "sweetness": {
                "enabled": True,
                "options": [
                    {"name": "Less Sweet", "price_modifier": 0},
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Sweet", "price_modifier": 0}
                ]
            },
            "mint": {
                "enabled": True,
                "options": [
                    {"name": "Regular Mint", "price_modifier": 0},
                    {"name": "Extra Mint", "price_modifier": 5}
                ]
            }
        }
    },
    {
        "name": "Masala Chai",
        "description": "Traditional spiced tea brewed with cardamom, ginger, and aromatic spices",
        "images": ["https://images.unsplash.com/photo-1570197788417-0e82375c9371?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwzfHxtYXNhbGElMjBjaGFpfGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "beverages",
        "base_price": 39.0,
        "stock_quantity": 180,
        "min_stock_level": 36,
        "preparation_time": 8,
        "tags": ["chai", "tea", "spiced", "ginger", "cardamom"],
        "customization_options": {
            "strength": {
                "enabled": True,
                "options": [
                    {"name": "Light", "price_modifier": 0},
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Strong", "price_modifier": 0}
                ]
            },
            "sweetness": {
                "enabled": True,
                "options": [
                    {"name": "Less Sweet", "price_modifier": 0},
                    {"name": "Regular", "price_modifier": 0},
                    {"name": "Extra Sweet", "price_modifier": 0}
                ]
            }
        }
    },

    # SNACKS (3 products)
    {
        "name": "Samosa",
        "description": "Crispy triangular pastry filled with spiced potatoes and peas, served with chutney",
        "images": ["https://images.unsplash.com/photo-1601050690597-df0568f70950?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxzYW1vc2F8ZW58MHx8fHwxNzU0MjExMTI3fDA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "snacks",
        "base_price": 35.0,
        "stock_quantity": 250,
        "min_stock_level": 50,
        "preparation_time": 12,
        "tags": ["samosa", "crispy", "pastry", "potato", "peas", "fried"],
        "customization_options": {
            "quantity": {
                "enabled": True,
                "options": [
                    {"name": "2 Pieces", "price_modifier": 0},
                    {"name": "4 Pieces", "price_modifier": 35},
                    {"name": "6 Pieces", "price_modifier": 65}
                ]
            },
            "chutney": {
                "enabled": True,
                "options": [
                    {"name": "Green Chutney", "price_modifier": 0},
                    {"name": "Tamarind Chutney", "price_modifier": 0},
                    {"name": "Both", "price_modifier": 10}
                ]
            }
        }
    },
    {
        "name": "Mixed Pakoras",
        "description": "Assorted vegetable fritters coated in spiced gram flour batter and deep-fried",
        "images": ["https://images.unsplash.com/photo-1601050690597-df0568f70950?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHxwYWtvcmFzfGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "snacks",
        "base_price": 89.0,
        "stock_quantity": 120,
        "min_stock_level": 24,
        "preparation_time": 15,
        "tags": ["pakoras", "fritters", "vegetables", "gram flour", "fried"],
        "customization_options": {
            "mix": {
                "enabled": True,
                "options": [
                    {"name": "Regular Mix", "price_modifier": 0},
                    {"name": "Onion Special", "price_modifier": 10},
                    {"name": "Paneer Mix", "price_modifier": 25}
                ]
            }
        }
    },
    {
        "name": "Vegetable Cutlets",
        "description": "Golden-fried patties made with mixed vegetables and spices, served with chutney",
        "images": ["https://images.unsplash.com/photo-1601050690597-df0568f70950?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwzfHx2ZWdldGFibGUlMjBjdXRsZXRzfGVufDB8fHx8fDE3NTQyMTExMjd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "snacks",
        "base_price": 99.0,
        "stock_quantity": 80,
        "min_stock_level": 16,
        "preparation_time": 18,
        "tags": ["cutlets", "vegetables", "patties", "fried", "spices"],
        "customization_options": {
            "quantity": {
                "enabled": True,
                "options": [
                    {"name": "2 Pieces", "price_modifier": 0},
                    {"name": "3 Pieces", "price_modifier": 30},
                    {"name": "4 Pieces", "price_modifier": 55}
                ]
            }
        }
    },

    # EXISTING PRODUCTS (8 products) - Enhanced with new fields
    {
        "name": "Buddha Bowl Delight",
        "description": "A colorful and nutritious vegan bowl packed with quinoa, roasted vegetables, avocado, and tahini dressing",
        "images": ["https://images.unsplash.com/photo-1599020792689-9fde458e7e17?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHx2ZWdldGFyaWFuJTIwZm9vZHxlbnwwfHx8fDE3NTQyMTExMTd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "international",
        "base_price": 299.0,
        "stock_quantity": 45,
        "min_stock_level": 9,
        "preparation_time": 20,
        "tags": ["buddha bowl", "quinoa", "healthy", "avocado", "tahini"],
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
        "subcategory": "international",
        "base_price": 329.0,
        "stock_quantity": 35,
        "min_stock_level": 7,
        "preparation_time": 22,
        "tags": ["power bowl", "protein", "superfoods", "energizing", "healthy"],
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
        "subcategory": "international",
        "base_price": 249.0,
        "stock_quantity": 55,
        "min_stock_level": 11,
        "preparation_time": 18,
        "tags": ["cauliflower", "hazelnuts", "salad", "roasted", "lemon"],
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
    {
        "name": "Traditional Tamil Thali",
        "description": "Authentic South Indian thali with rice, dal, vegetables, pickles, and traditional accompaniments",
        "images": ["https://images.unsplash.com/photo-1742281258189-3b933879867a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHwyfHxpbmRpYW4lMjB2ZWdldGFyaWFufGVufDB8fHx8MTc1NDIxMTEyN3ww&ixlib=rb-4.1.0&q=85"],
        "category": "vegetarian",
        "subcategory": "south-indian",
        "base_price": 349.0,
        "stock_quantity": 30,
        "min_stock_level": 6,
        "preparation_time": 25,
        "tags": ["thali", "traditional", "tamil", "complete meal", "authentic"],
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
        "subcategory": "south-indian",
        "base_price": 449.0,
        "stock_quantity": 25,
        "min_stock_level": 5,
        "preparation_time": 30,
        "tags": ["festival", "special", "elaborate", "seasonal", "festive"],
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
        "subcategory": "north-indian",
        "base_price": 399.0,
        "stock_quantity": 35,
        "min_stock_level": 7,
        "preparation_time": 28,
        "tags": ["complete", "thali", "traditional", "full meal", "indian"],
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
    {
        "name": "Fresh Garden Salad",
        "description": "Crisp mixed greens with seasonal vegetables, nuts, and house-made dressing",
        "images": ["https://images.unsplash.com/photo-1615366105533-5b8f3255ea5d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwzfHx2ZWdldGFyaWFuJTIwZm9vZHxlbnwwfHx8fDE3NTQyMTExMTd8MA&ixlib=rb-4.1.0&q=85"],
        "category": "vegan",
        "subcategory": "international",
        "base_price": 199.0,
        "stock_quantity": 100,
        "min_stock_level": 20,
        "preparation_time": 12,
        "tags": ["fresh", "salad", "greens", "seasonal", "healthy"],
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
        "subcategory": "international",
        "base_price": 279.0,
        "stock_quantity": 60,
        "min_stock_level": 12,
        "preparation_time": 15,
        "tags": ["protein", "salad", "nutritious", "superfoods", "plant-based"],
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