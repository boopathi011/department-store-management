from database.mongo_service import MongoService
from config import Config
from utils.auth_middleware import generate_token
from pymongo.errors import PyMongoError

class AuthController:
    @staticmethod
    def login(username, password):
        try:
            user = MongoService.find_one('users', {"username": username, "password": password})
            if user:
                token = generate_token(username, user['role'])
                return {"status": "ok", "role": user["role"], "token": token, "username": username}, 200
            return {"status": "fail", "message": "Invalid credentials"}, 401
        except PyMongoError as e:
            return {"status": "error", "message": "Database connection error"}, 500

    @staticmethod
    def register(username, password, name, role='user'):
        try:
            if MongoService.find_one('users', {"username": username}):
                return {"status": "fail", "message": "User already exists"}, 400
            
            new_user = {
                "username": username,
                "password": password,
                "name": name,
                "role": role,
                "loan_eligible": False # Default to false, admin must enable
            }
            result = MongoService.insert_one('users', new_user)
            if result.acknowledged:
                return {"status": "ok", "message": "User registered"}, 201
            return {"status": "fail", "message": "Error saving user"}, 500
        except PyMongoError as e:
            return {"status": "error", "message": "Database connection error"}, 500
