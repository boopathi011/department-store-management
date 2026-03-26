from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoService:
    client = None
    db = None

    @classmethod
    def get_db(cls):
        try:
            if cls.db is None:
                if cls.client is None:
                    logger.info(f"Connecting to MongoDB...")
                    cls.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
                    # Force a connection check
                    cls.client.admin.command('ping')
                    logger.info("Successfully connected to MongoDB")
                cls.db = cls.client[Config.DATABASE_NAME]
            return cls.db
        except (ConnectionFailure, PyMongoError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            cls.db = None
            cls.client = None
            return None

    @classmethod
    def get_collection(cls, collection_name):
        db = cls.get_db()
        if db is not None:
            return db[collection_name]
        return None

    @classmethod
    def find_all(cls, collection_name, filter_query=None):
        coll = cls.get_collection(collection_name)
        if coll is None:
            raise PyMongoError("Database connection unavailable")
        query = filter_query if filter_query else {}
        return list(coll.find(query, {"_id": 0}))

    @classmethod
    def find_one(cls, collection_name, query):
        coll = cls.get_collection(collection_name)
        if coll is None:
            raise PyMongoError("Database connection unavailable")
        return coll.find_one(query, {"_id": 0})

    @classmethod
    def insert_one(cls, collection_name, data):
        coll = cls.get_collection(collection_name)
        if coll is None:
            raise PyMongoError("Database connection unavailable")
        return coll.insert_one(data.copy())

    @classmethod
    def update_one(cls, collection_name, query, data):
        coll = cls.get_collection(collection_name)
        if coll is None:
            raise PyMongoError("Database connection unavailable")
        return coll.update_one(query, {"$set": data})

    @classmethod
    def delete_one(cls, collection_name, query):
        coll = cls.get_collection(collection_name)
        if coll is None:
            raise PyMongoError("Database connection unavailable")
        return coll.delete_one(query)
