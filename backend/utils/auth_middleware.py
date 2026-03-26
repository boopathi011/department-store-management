import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # Token format: "Bearer <token>"
            data = jwt.decode(token.split(" ")[1], Config.SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']
            role = data['role']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, role, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, role, *args, **kwargs):
        if role != 'admin':
            return jsonify({'message': 'Admin access required!'}), 403
        return f(current_user, role, *args, **kwargs)
    return decorated

def generate_token(username, role):
    return jwt.encode({
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, Config.SECRET_KEY, algorithm="HS256")
