import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.mongo_service import MongoService

def test_conn():
    try:
        products = MongoService.find_all('products')
        if products:
            print(f"Sucessfully connected. Found {len(products)} products in MongoDB.")
            print(f"First product sample: {products[0]['name']}")
        else:
            print("Successfully connected, but no products found in database.")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    test_conn()
