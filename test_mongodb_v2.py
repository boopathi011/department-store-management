from pymongo import MongoClient
import os
import sys

# Add backend to path to import Config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
from config import Config

def test_connection():
    print(f"Testing connection to: {Config.MONGO_URI}")
    try:
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("MongoDB connection successful!")
        
        db = client[Config.DATABASE_NAME]
        print(f"Using database: {Config.DATABASE_NAME}")
        
        collections = db.list_collection_names()
        print(f"Collections: {collections}")
        
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

if __name__ == "__main__":
    test_connection()
