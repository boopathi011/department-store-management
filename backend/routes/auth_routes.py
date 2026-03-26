from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    result, status = AuthController.login(data.get('username'), data.get('password'))
    return jsonify(result), status

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    result, status = AuthController.register(
        data.get('username'), 
        data.get('password'), 
        data.get('name'), 
        data.get('role', 'user')
    )
    return jsonify(result), status
