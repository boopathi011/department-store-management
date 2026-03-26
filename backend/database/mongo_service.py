from pymongo import MongoClient
from config import Config

class MongoService:
    client = None
    db = None

    @classmethod
    def get_db(cls):
        if cls.db is None:
            if cls.client is None:
                cls.client = MongoClient(Config.MONGO_URI)
            cls.db = cls.client[Config.DATABASE_NAME]
        return cls.db

    @classmethod
    def get_collection(cls, collection_name):
        return cls.get_db()[collection_name]

    @classmethod
    def find_all(cls, collection_name, filter_query=None):
        query = filter_query if filter_query else {}
        return list(cls.get_collection(collection_name).find(query, {"_id": 0}))

    @classmethod
    def find_one(cls, collection_name, query):
        return cls.get_collection(collection_name).find_one(query, {"_id": 0})

    @classmethod
    def insert_one(cls, collection_name, data):
        return cls.get_collection(collection_name).insert_one(data.copy())

    @classmethod
    def update_one(cls, collection_name, query, data):
        return cls.get_collection(collection_name).update_one(query, {"$set": data})

    @classmethod
    def delete_one(cls, collection_name, query):
        return cls.get_collection(collection_name).delete_one(query)
