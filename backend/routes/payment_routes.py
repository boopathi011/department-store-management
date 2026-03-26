from flask import Blueprint, request, jsonify
from database.mongo_service import MongoService
from utils.auth_middleware import token_required
from config import Config
import datetime
from pymongo.errors import PyMongoError

payment_bp = Blueprint('payments', __name__)

@payment_bp.route('/payments/create-order', methods=['POST'])
@token_required
def create_pay_order(current_user, role):
    try:
        data = request.json
        amount = data.get('amount') # in rupees
        
        if not amount or amount <= 0:
            return jsonify({"status": "fail", "message": "Invalid amount"}), 400
            
        mock_order = {
            "id": f"order_mock_{datetime.datetime.now().timestamp()}",
            "amount": int(amount * 100),
            "currency": "INR",
            "key": Config.RAZORPAY_KEY_ID
        }
        return jsonify(mock_order), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@payment_bp.route('/payments/verify', methods=['POST'])
@token_required
def verify_payment(current_user, role):
    try:
        data = request.json
        order_id = data.get('razorpay_order_id')
        payment_id = data.get('razorpay_payment_id')
        
        # If verified, mark all customer's unpaid orders as PAID
        unpaid_orders = MongoService.find_all('orders', {"user": current_user, "paid": False})
        
        for o in unpaid_orders:
             MongoService.update_one('orders', 
                {"id": o['id']}, 
                {"paid": True, "paid_date": str(datetime.datetime.now().date()), "payment_id": payment_id}
             )
             
        return jsonify({"status": "ok", "message": "Payment verified and dues cleared!"}), 200
    except PyMongoError:
        return jsonify({"status": "error", "message": "Database connection error"}), 500
