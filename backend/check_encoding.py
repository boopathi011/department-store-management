from services.file_service import FileService
from config import Config
import os

files = [Config.USERS_FILE, Config.PRODUCTS_FILE, Config.ORDERS_FILE, Config.LOANS_FILE]
for f in files:
    print(f"Checking {f}...")
    data = FileService.read_json(f)
    print(f"Successfully read {len(data)} items.")

print("All files read successfully.")
