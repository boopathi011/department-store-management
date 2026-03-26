from flask import Blueprint, request, jsonify
from database.mongo_service import MongoService
from config import Config
from utils.auth_middleware import token_required, admin_required
import datetime
from pymongo.errors import PyMongoError

loan_bp = Blueprint('loans', __name__)

@loan_bp.route('/loans/active', methods=['GET'])
@token_required
def get_active_loans(current_user, role):
    try:
        user_loans = MongoService.find_all('orders', {"user": current_user, "paid": False})
        return jsonify(user_loans), 200
    except PyMongoError:
        return jsonify({"status": "error", "message": "Database connection error"}), 500

@loan_bp.route('/admin/loans', methods=['GET'])
@token_required
@admin_required
def get_all_loans(current_user, role):
    try:
        all_loans = MongoService.find_all('orders', {"paid": False})
        return jsonify(all_loans), 200
    except PyMongoError:
        return jsonify({"status": "error", "message": "Database connection error"}), 500

@loan_bp.route('/admin/loans', methods=['POST'])
@token_required
@admin_required
def create_manual_loan(current_user, role):
    try:
        data = request.json
        username = data.get('username')
        product_id = data.get('product_id')
        deadline_days = data.get('deadline_days', Config.LOAN_REPAYMENT_DAYS)
        
        user = MongoService.find_one('users', {"username": username})
        if not user:
            return jsonify({"status": "fail", "message": "User not found"}), 404
            
        product = MongoService.find_one('products', {'id': int(product_id)})
        if not product:
            return jsonify({"status": "fail", "message": "Product not found"}), 404
            
        orders = MongoService.find_all('orders')
        new_id = max([o.get('id', 0) for o in orders]) + 1 if orders else 1
        
        new_loan = {
            "id": new_id,
            "user": username,
            "product": int(product_id),
            "product_name": product['name'],
            "price": product['price'],
            "date": str(datetime.date.today()),
            "paid": False,
            "is_loan": True,
            "deadline_days": deadline_days
        }
        
        result = MongoService.insert_one('orders', new_loan)
        if result.acknowledged:
            return jsonify({"status": "ok", "message": "Loan created manually"}), 201
        return jsonify({"status": "fail", "message": "Error creating loan"}), 500
    except PyMongoError:
        return jsonify({"status": "error", "message": "Database connection error"}), 500

@loan_bp.route('/admin/reminders/send', methods=['POST'])
@token_required
@admin_required
def send_reminder(current_user, role):
    try:
        data = request.json
        order_id = data.get('order_id')
        
        result = MongoService.update_one('orders', {'id': int(order_id)}, {'reminder_sent_at': str(datetime.datetime.now())})
        if result.modified_count > 0 or result.matched_count > 0:
            return jsonify({"status": "ok", "message": f"Reminder sent successfully"}), 200
        return jsonify({"status": "fail", "message": "Order not found or update failed"}), 404
    except PyMongoError:
        return jsonify({"status": "error", "message": "Database connection error"}), 500
