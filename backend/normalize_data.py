import json
import os

ORDERS_FILE = r'd:\department-store\backend\database\orders.json'

if os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, 'r') as f:
        orders = json.load(f)
    
    for o in orders:
        if 'product' in o:
            try:
                o['product'] = int(o['product'])
            except:
                pass
                
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=4)
    print("Normalized orders.json")
else:
    print("Orders file not found")
