from flask import Blueprint, request, jsonify
from controllers.order_controller import OrderController
from database.mongo_service import MongoService
from config import Config
from utils.auth_middleware import token_required, admin_required
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
@token_required
@admin_required
def get_all_users(current_user, role):
    users = MongoService.find_all('users')
    return jsonify([{k: v for k, v in u.items() if k != 'password'} for u in users]), 200

@admin_bp.route('/admin/users/toggle_loan', methods=['POST'])
@token_required
@admin_required
def toggle_loan(current_user, role):
    data = request.json
    username = data.get('username')
    user = MongoService.find_one('users', {"username": username})
    
    if user:
        new_status = not user.get('loan_eligible', False)
        MongoService.update_one('users', {"username": username}, {'loan_eligible': new_status})
        return jsonify({"status": "ok", "loan_eligible": new_status}), 200
            
    return jsonify({"status": "fail", "message": "User not found"}), 404

@admin_bp.route('/admin/orders', methods=['GET'])
@token_required
@admin_required
def get_all_orders(current_user, role):
    return jsonify(OrderController.get_all_orders()), 200

@admin_bp.route('/admin/stats', methods=['GET'])
@token_required
@admin_required
def get_stats(current_user, role):
    orders = OrderController.get_all_orders()
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    today_str = today.strftime("%Y-%m-%d")
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    current_month_str = today.strftime("%Y-%m")
    current_year_str = today.strftime("%Y")

    total_sales = 0
    daily_sales = 0
    yesterday_sales = 0
    monthly_sales = 0
    yearly_sales = 0

    unpaid_orders = []

    for o in orders:
        price = o.get('price', 0)
        order_date_str = o.get('paid_date', o.get('date', ""))
        
        if o.get('paid', False):
            total_sales += price
            if order_date_str.startswith(today_str):
                daily_sales += price
            elif order_date_str.startswith(yesterday_str):
                yesterday_sales += price
            
            if order_date_str.startswith(current_month_str):
                monthly_sales += price
            if order_date_str.startswith(current_year_str):
                yearly_sales += price
        else:
            unpaid_orders.append(o)

    active_loans = len(unpaid_orders)
    pending_recovery = sum(o.get('price', 0) for o in unpaid_orders)
    
    return jsonify({
        "total_sales": total_sales,
        "daily_sales": daily_sales,
        "yesterday_sales": yesterday_sales,
        "monthly_sales": monthly_sales,
        "yearly_sales": yearly_sales,
        "active_loans": active_loans,
        "pending_recovery": pending_recovery,
        "server_date": today_str,
        "recent_activity": orders[-50:] if orders else []
    }), 200

@admin_bp.route('/admin/orders/pay', methods=['POST'])
@token_required
@admin_required
def mark_order_paid(current_user, role):
    data = request.json
    order_id = data.get('order_id')
    
    if MongoService.update_one('orders', {'id': order_id}, {'paid': True, 'paid_date': str(datetime.now().date())}):
        return jsonify({"status": "ok", "message": "Order marked as received!"}), 200
            
    return jsonify({"status": "fail", "message": "Order not found"}), 404
