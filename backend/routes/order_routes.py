from flask import Blueprint, request, jsonify
from controllers.order_controller import OrderController
from utils.auth_middleware import token_required

order_bp = Blueprint('orders', __name__)

@order_bp.route('/order', methods=['POST'])
@token_required
def create_order(current_user, role):
    data = request.json
    result, status = OrderController.create_order(current_user, data)
    return jsonify(result), status

@order_bp.route('/user/orders', methods=['GET'])
@token_required
def get_user_orders(current_user, role):
    result, status = OrderController.get_user_orders(current_user)
    return jsonify(result), status

@order_bp.route('/user/stats', methods=['GET'])
@token_required
def get_user_stats(current_user, role):
    result, status = OrderController.get_user_stats(current_user)
    return jsonify(result), status
