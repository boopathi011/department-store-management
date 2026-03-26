import json

def fix_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Products
products = [
    {"id": 1, "name": "Fresh Appples (500g)", "price": 120, "category": "Groceries", "image": "🍎"},
    {"id": 2, "name": "Banana Bunch", "price": 60, "category": "Groceries", "image": "🍌"},
    {"id": 3, "name": "Organic Milk (1L)", "price": 85, "category": "Groceries", "image": "🥛"},
    {"id": 4, "name": "Whole Wheat Bread", "price": 45, "category": "Groceries", "image": "🍞"},
    {"id": 5, "name": "Greek Yogurt (200g)", "price": 40, "category": "Groceries", "image": "🍦"},
    {"id": 6, "name": "Detergent Powder (1kg)", "price": 250, "category": "Household", "image": "🧼"},
    {"id": 7, "name": "Dishwashing Liquid", "price": 95, "category": "Household", "image": "🧴"},
    {"id": 8, "name": "Kitchen Tissue Roll", "price": 110, "category": "Household", "image": "🧻"},
    {"id": 9, "name": "Sparkling Water", "price": 75, "category": "Groceries", "image": "🫧"},
    {"id": 10, "name": "Dark Chocolate 70%", "price": 180, "category": "Groceries", "image": "🍫"},
    {"id": 11, "name": "Toilet Cleaner (500ml)", "price": 130, "category": "Household", "image": "🚽"},
    {"id": 12, "name": "Floor Cleaner (1L)", "price": 190, "category": "Household", "image": "🧹"},
    {"id": 13, "name": "Liquid Hand Wash", "price": 145, "category": "Personal Care", "image": "🧼"},
    {"id": 14, "name": "Shampoo Premium", "price": 320, "category": "Personal Care", "image": "🧴"},
    {"id": 15, "name": "Toothpaste (150g)", "price": 95, "category": "Personal Care", "image": "🪥"},
    {"id": 16, "name": "Face Wash (Aloe)", "price": 210, "category": "Personal Care", "image": "🫧"},
    {"id": 17, "name": "Cotton Swabs (100pk)", "price": 50, "category": "Personal Care", "image": "👂"},
    {"id": 18, "name": "Green Tea (25 Bags)", "price": 260, "category": "Groceries", "image": "🍵"},
    {"id": 19, "name": "Coffee Beans (250g)", "price": 450, "category": "Groceries", "image": "☕"},
    {"id": 20, "name": "Cooking Oil (1L)", "price": 185, "category": "Groceries", "image": "🫗"},
    {"id": 21, "name": "Basmati Rice (5kg)", "price": 750, "category": "Groceries", "image": "🍚"},
    {"id": 22, "name": "Pasta Fusilli (500g)", "price": 135, "category": "Groceries", "image": "🍝"},
    {"id": 23, "name": "Tomato Ketchup", "price": 120, "category": "Groceries", "image": "🥫"},
    {"id": 24, "name": "Laundry Fabric Softener", "price": 280, "category": "Household", "image": "🌸"},
    {"id": 25, "name": "Aluminum Foil", "price": 160, "category": "Household", "image": "📄"},
    {"id": 26, "name": "Dusting Cloth (3pk)", "price": 140, "category": "Household", "image": "🧹"},
    {"id": 27, "name": "Shower Gel (Lemon)", "price": 290, "category": "Personal Care", "image": "🚿"},
    {"id": 28, "name": "Mouthwash (500ml)", "price": 240, "category": "Personal Care", "image": "🦷"},
    {"id": 29, "name": "Sunscreen SPF 50", "price": 550, "category": "Personal Care", "image": "☀️"},
    {"id": 30, "name": "Body Lotion (Cocoa)", "price": 380, "category": "Personal Care", "image": "🧴"}
]

# Users
users = [
    { "username": "admin", "password": "admin123", "role": "admin", "loan_eligible": True },
    { "username": "user", "password": "123", "role": "user", "loan_eligible": False },
    { "username": "boopathi", "password": "boopathi2005", "name": "BOOPATHI R", "role": "user", "loan_eligible": True }
]

fix_file('database/products.json', products)
fix_file('database/users.json', users)
fix_file('database/orders.json', [])
fix_file('database/loans.json', [])

print("All JSON files repaired in UTF-8.")
