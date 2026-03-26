import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.mongo_service import MongoService

def debug_mongo():
    print("--- Detailed MongoDB Diagnostics ---")
    try:
        db = MongoService.get_db()
        print(f"Connected to Database: {db.name}")
        
        collections = db.list_collection_names()
        print(f"Collections present: {collections}")
        
        for coll_name in ['users', 'products', 'orders', 'loans']:
            count = MongoService.get_collection(coll_name).count_documents({})
            print(f" - Collection '{coll_name}': {count} documents")
            if count > 0:
                sample = MongoService.find_one(coll_name, {})
                print(f"   Sample from '{coll_name}': {sample.get('id') or sample.get('username')}")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_mongo()
