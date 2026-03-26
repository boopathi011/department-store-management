from flask import Blueprint, request, jsonify
from database.mongo_service import MongoService
from utils.auth_middleware import token_required
from config import Config
import datetime

payment_bp = Blueprint('payments', __name__)

@payment_bp.route('/payments/create-order', methods=['POST'])
@token_required
def create_pay_order(current_user, role):
    data = request.json
    amount = data.get('amount') # in rupees
    
    if not amount or amount <= 0:
        return jsonify({"status": "fail", "message": "Invalid amount"}), 400
        
    # In a real app with 'razorpay' package:
    # client = razorpay.Client(auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET))
    # order = client.order.create({
    #     'amount': int(amount * 100), # paise
    #     'currency': 'INR',
    #     'payment_capture': '1'
    # })
    # return jsonify(order), 200
    
    # MOCK Order for now
    mock_order = {
        "id": f"order_mock_{datetime.datetime.now().timestamp()}",
        "amount": int(amount * 100),
        "currency": "INR",
        "key": Config.RAZORPAY_KEY_ID
    }
    return jsonify(mock_order), 200

@payment_bp.route('/payments/verify', methods=['POST'])
@token_required
def verify_payment(current_user, role):
    data = request.json
    order_id = data.get('razorpay_order_id')
    payment_id = data.get('razorpay_payment_id')
    
    # In a real app, verify signature:
    # client.utility.verify_payment_signature(data)
    
    # If verified, mark all customer's unpaid orders as PAID
    unpaid_orders = MongoService.find_all('orders', {"user": current_user, "paid": False})
    
    for o in unpaid_orders:
         MongoService.update_one('orders', 
            {"id": o['id']}, 
            {"paid": True, "paid_date": str(datetime.datetime.now().date()), "payment_id": payment_id}
         )
         
    return jsonify({"status": "ok", "message": "Payment verified and dues cleared!"}), 200
