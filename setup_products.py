import json
import random

def generate_products():
    categories_data = {
        "Groceries": [
            ("Fresh Apples (1kg)", 150),
            ("Banana Bunch (1 Dozen)", 60),
            ("Organic Milk (1L)", 85),
            ("Whole Wheat Bread", 50),
            ("Greek Yogurt (200g)", 45),
            ("Sparkling Water (1L)", 75),
            ("Dark Chocolate 70%", 180),
            ("Green Tea (25 Bags)", 260),
            ("Coffee Beans (250g)", 450),
            ("Cooking Oil (1L)", 185),
            ("Basmati Rice (5kg)", 750),
            ("Pasta Fusilli (500g)", 135),
            ("Tomato Ketchup", 120),
            ("Brown Sugar (1kg)", 90),
            ("Rolled Oats (1kg)", 200),
            ("Honey (500g)", 250),
            ("Peanut Butter (340g)", 199),
            ("Almonds (500g)", 550),
            ("Walnuts (250g)", 400),
            ("Cashews (500g)", 600),
            ("Raisins (500g)", 300),
            ("Pistachios (250g)", 500)
        ],
        "Pulses": [
            ("Toor Dal (1kg)", 160),
            ("Moong Dal (1kg)", 120),
            ("Urad Dal (1kg)", 140),
            ("Chana Dal (1kg)", 110),
            ("Masoor Dal (1kg)", 100),
            ("Rajma (Kidney Beans 1kg)", 180),
            ("Kabuli Chana (Chickpeas 1kg)", 160),
            ("Green Gram (1kg)", 130),
            ("Black Gram (1kg)", 140),
            ("Lobia (Black-eyed Peas 1kg)", 150)
        ],
        "Spices": [
            ("Turmeric Powder (200g)", 60),
            ("Red Chilli Powder (200g)", 80),
            ("Coriander Powder (200g)", 70),
            ("Cumin Seeds (Jeera 100g)", 90),
            ("Mustard Seeds (100g)", 40),
            ("Garam Masala (100g)", 110),
            ("Black Pepper (100g)", 150),
            ("Cloves (50g)", 120),
            ("Cardamom (50g)", 200),
            ("Cinnamon Sticks (50g)", 80),
            ("Fenugreek Seeds (100g)", 50),
            ("Fennel Seeds (100g)", 60),
            ("Asafoetida (Hing 50g)", 75),
            ("Bay Leaves (50g)", 40),
            ("Nutmeg (50g)", 100)
        ],
        "Snacks": [
            ("Potato Chips (Salted)", 20),
            ("Potato Chips (Spicy)", 20),
            ("Nachos (Cheese)", 50),
            ("Roasted Peanuts", 40),
            ("Mixed Namkeen (400g)", 120),
            ("Aloo Bhujia (400g)", 110),
            ("Khakhra", 60),
            ("Diet Chivda (200g)", 80),
            ("Popcorn (Butter)", 30),
            ("Cookies (Choco Chip)", 60),
            ("Digestive Biscuits", 50),
            ("Crackers (Salted)", 40),
            ("Protein Bar", 80),
            ("Dry Fruit Ladoo", 150),
            ("Roasted Makhana", 90)
        ],
        "Beverages": [
            ("Cola (1.5L)", 90),
            ("Lemon Soda (1.5L)", 85),
            ("Orange Juice (1L)", 110),
            ("Apple Juice (1L)", 110),
            ("Mixed Fruit Juice (1L)", 120),
            ("Cold Coffee (Can)", 60),
            ("Energy Drink", 110),
            ("Almond Milk (1L)", 250),
            ("Soy Milk (1L)", 150),
            ("Oat Milk (1L)", 280),
            ("Buttermilk", 20),
            ("Lassi (Mango)", 40)
        ],
        "Personal Care": [
            ("Liquid Hand Wash", 145),
            ("Shampoo Premium (400ml)", 320),
            ("Conditioner (200ml)", 200),
            ("Toothpaste (150g)", 95),
            ("Toothbrush (Pack of 4)", 120),
            ("Face Wash (Aloe)", 210),
            ("Cotton Swabs (100pk)", 50),
            ("Shower Gel (Lemon)", 290),
            ("Mouthwash (500ml)", 240),
            ("Sunscreen SPF 50", 550),
            ("Body Lotion (Cocoa)", 380),
            ("Deodorant Spray", 250),
            ("Hair Oil (Coconut 500ml)", 180),
            ("Shaving Cream", 110),
            ("Razors (Pack of 5)", 200),
            ("Wet Wipes (80pcs)", 150),
            ("Talcum Powder", 130),
            ("Lip Balm", 80)
        ],
        "Household": [
            ("Detergent Powder (1kg)", 250),
            ("Dishwashing Liquid", 95),
            ("Kitchen Tissue Roll", 110),
            ("Toilet Cleaner (500ml)", 130),
            ("Floor Cleaner (1L)", 190),
            ("Laundry Fabric Softener", 280),
            ("Aluminum Foil", 160),
            ("Dusting Cloth (3pk)", 140),
            ("Trash Bags (30pcs)", 120),
            ("Room Freshener", 150),
            ("Mosquito Repellent Liquid", 85),
            ("Glass Cleaner (500ml)", 110),
            ("Sponges (Pack of 3)", 60),
            ("Toilet Paper (4 Rolls)", 180),
            ("Batteries AA (Pack of 4)", 100)
        ],
        "Dairy": [
            ("Paneer (200g)", 90),
            ("Butter (100g)", 55),
            ("Cheese Slices (200g)", 140),
            ("Cheese Block (200g)", 130),
            ("Curd (400g)", 45),
            ("Fresh Cream (200ml)", 70),
            ("Ghee (500ml)", 350)
        ]
    }

    # Helper function to get a random unsplash image link (using a generic search query or ids if preferred, 
    # but here we use generic nice placeholders for food/groceries)
    base_images = [
        "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=300&q=80",
        "https://images.unsplash.com/photo-1506484381205-f9bcf56b8142?auto=format&fit=crop&w=300&q=80",
        "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=300&q=80",
        "https://images.unsplash.com/photo-1588600878108-578307a3cc9d?auto=format&fit=crop&w=300&q=80",
        "https://images.unsplash.com/photo-1543168256-418811576931?auto=format&fit=crop&w=300&q=80",
        "https://images.unsplash.com/photo-1606859191214-25806e8e2423?auto=format&fit=crop&w=300&q=80"
    ]

    products = []
    current_id = 1

    for category, items in categories_data.items():
        for name, price in items:
            image_url = random.choice(base_images)
            
            # You can customize images per category if preferred, but random nice food images work for a mockup
            if category == "Personal Care" or category == "Household":
                image_url = "https://images.unsplash.com/photo-1583947215259-38e31be8751f?auto=format&fit=crop&w=300&q=80" # Generic cleaning/care type image
            
            products.append({
                "id": current_id,
                "name": name,
                "price": price,
                "category": category,
                "image": image_url
            })
            current_id += 1

    with open('backend/database/products.json', 'w') as f:
        json.dump(products, f, indent=4)
        
    print(f"Successfully generated {len(products)} products across {len(categories_data)} categories.")

if __name__ == "__main__":
    generate_products()
