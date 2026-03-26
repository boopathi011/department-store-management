import os
import sys

# Add backend to path to import Config and FileService
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from services.file_service import FileService
from database.mongo_service import MongoService

def migrate_data():
    collections_map = {
        Config.USERS_FILE: 'users',
        Config.PRODUCTS_FILE: 'products',
        Config.ORDERS_FILE: 'orders',
        Config.LOANS_FILE: 'loans'
    }

    print("Starting data migration to MongoDB...")

    for file_path, collection_name in collections_map.items():
        if os.path.exists(file_path):
            data = FileService.read_json(file_path)
            if data:
                collection = MongoService.get_collection(collection_name)
                # Clear existing data in collection before migration to avoid duplicates
                collection.delete_many({})
                collection.insert_many(data)
                print(f"Migrated {len(data)} items from {os.path.basename(file_path)} to {collection_name} collection.")
            else:
                print(f"No data found in {os.path.basename(file_path)}.")
        else:
            print(f"File {os.path.basename(file_path)} not found. Skipping.")

    print("Migration completed successfully.")

if __name__ == "__main__":
    migrate_data()
