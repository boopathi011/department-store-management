from flask import Blueprint, jsonify, request
from database.mongo_service import MongoService
from config import Config
from utils.auth_middleware import token_required, admin_required
import datetime

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/admin/analytics/products', methods=['GET'])
@token_required
@admin_required
def product_analytics(current_user, role):
    period = request.args.get('period', 'monthly').lower()
    orders = MongoService.find_all('orders')
    products = MongoService.find_all('products')
    
    # Filter orders by period
    today = datetime.date.today()
    if period == 'daily':
        start_date = today
    elif period == 'weekly':
        start_date = today - datetime.timedelta(days=today.weekday())
    else: # monthly
        start_date = today.replace(day=1)
        
    try:
        filtered_orders = [o for o in orders if datetime.date.fromisoformat(o['date']) >= start_date]
    except Exception:
        # Fallback if date is not in perfect ISO format
        filtered_orders = [o for o in orders if o.get('date', '').split('T')[0] >= start_date.isoformat()]
    
    # Calculate sales frequencies
    sales_count = {}
    for o in filtered_orders:
        pid = str(o['product'])
        sales_count[pid] = sales_count.get(pid, 0) + 1
        
    sorted_sales = sorted(sales_count.items(), key=lambda x: x[1], reverse=True)
    
    top_products = []
    for pid, count in sorted_sales[:5]:
        p = next((x for x in products if str(x['id']) == pid), None)
        if p: top_products.append({"name": p['name'], "sales": count})
        
    least_products = []
    # Any product not in sales_count or at the bottom
    for p in products:
        if str(p['id']) not in sales_count:
            least_products.append({"name": p['name'], "sales": 0, "recommendation": "High price or low visibility. Consider a 10% discount."})
            if len(least_products) >= 5: break
            
    return jsonify({
        "top_selling": top_products,
        "least_selling": least_products,
        "period": period.capitalize()
    }), 200

@analytics_bp.route('/admin/analytics/customers', methods=['GET'])
@token_required
@admin_required
def customer_analytics(current_user, role):
    from models.predict import predict_customer
    users = MongoService.find_all('users', {"role": "user"})
    orders = MongoService.find_all('orders')
    
    customer_data = []
    for u in users:
        user_orders = [o for o in orders if o['user'] == u['username']]
        total_spend = sum(o.get('price', 0) for o in user_orders)
        order_count = len(user_orders)
        
        # Mocking visits and views for the prediction model since they aren't tracked yet
        visits = order_count * 2 + 5 
        views = order_count * 5 + 10
        discount_used = 1 if any(o.get('discount') for o in user_orders) else 0
        
        segment = predict_customer(visits, total_spend, order_count, views, discount_used)
        
        customer_data.append({
            "username": u['username'],
            "name": u.get('name', u['username']),
            "total_spend": total_spend,
            "order_count": order_count,
            "segment": segment
        })
        
    loyalty_list = sorted(customer_data, key=lambda x: x['total_spend'], reverse=True)[:5]
    
    total_customers = len(customer_data)
    if total_customers == 0:
        segments = {"Top Customer": 0, "Normal Customer": 0}
    else:
        segments = {
            "Top Customer": len([c for c in customer_data if c['segment'] == "Top Customer"]) / total_customers * 100,
            "Normal Customer": len([c for c in customer_data if c['segment'] == "Normal Customer"]) / total_customers * 100
        }
        
    return jsonify({
        "loyalty_members": loyalty_list,
        "segments": segments,
        "total_customers": total_customers
    }), 200

@analytics_bp.route('/admin/analytics/purchases', methods=['GET'])
@token_required
@admin_required
def purchase_analytics(current_user, role):
    orders = MongoService.find_all('orders')
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    
    # helper to get revenue for a specific date
    def get_revenue_for_date(date_obj):
        target = date_obj.strftime("%Y-%m-%d")
        return sum(o.get('price', 0) for o in orders if o.get('paid', False) and (o.get('paid_date', o.get('date', "")).startswith(target)))

    # 1. Daily Aggregation (Last 7 days revenue)
    daily_labels = []
    daily_values = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        daily_labels.append(date.strftime('%a'))
        daily_values.append(get_revenue_for_date(date))

    # 2. Monthly Aggregation (Current Year revenue)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_values = []
    for m_idx, m_name in enumerate(months):
        revenue = 0
        target_month_str = f"{today.year}-{str(m_idx+1).zfill(2)}"
        for o in orders:
            if not o.get('paid', False): continue
            o_date_str = o.get('paid_date', o.get('date', ""))
            if o_date_str.startswith(target_month_str):
                revenue += o.get('price', 0)
        monthly_values.append(revenue)
            
    # 3. Yearly Aggregation (Last 5 years revenue)
    yearly_labels = []
    yearly_values = []
    for i in range(4, -1, -1):
        year_str = str(today.year - i)
        yearly_labels.append(year_str)
        revenue = 0
        for o in orders:
            if not o.get('paid', False): continue
            o_date_str = o.get('paid_date', o.get('date', ""))
            if o_date_str.startswith(year_str):
                revenue += o.get('price', 0)
        yearly_values.append(revenue)

    # 4. Comparative Metrics
    today_sales = get_revenue_for_date(today)
    yesterday_sales = get_revenue_for_date(yesterday)
    
    this_year_sales = sum(o.get('price', 0) for o in orders if o.get('paid', False) and o.get('paid_date', o.get('date', "")).startswith(str(today.year)))
    last_year_sales = sum(o.get('price', 0) for o in orders if o.get('paid', False) and o.get('paid_date', o.get('date', "")).startswith(str(today.year - 1)))

    return jsonify({
        "daily": {"labels": daily_labels, "values": daily_values},
        "monthly": {"labels": months, "values": monthly_values},
        "yearly": {"labels": yearly_labels, "values": yearly_values},
        "comparisons": {
            "today": today_sales,
            "yesterday": yesterday_sales,
            "this_year": this_year_sales,
            "last_year": last_year_sales
        }
    }), 200
