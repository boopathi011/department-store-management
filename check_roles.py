import sys
import os

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(backend_dir)

from database.mongo_service import MongoService

def debug_users():
    users = MongoService.find_all('users')
    for u in users:
        print(f"User: {u.get('username')}, Role: '{u.get('role')}'")

if __name__ == "__main__":
    debug_users()
