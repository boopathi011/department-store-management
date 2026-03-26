import os
from dotenv import load_dotenv
import sys

# Add backend to path to import Config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
from config import Config

def check_env():
    load_dotenv()
    uri = os.environ.get('MONGO_URI')
    print(f"Environment MONGO_URI: {uri}")
    print(f"Config MONGO_URI: {Config.MONGO_URI}")

if __name__ == "__main__":
    check_env()
