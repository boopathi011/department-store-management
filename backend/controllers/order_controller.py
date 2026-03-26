import datetime
from database.mongo_service import MongoService
from config import Config

class OrderController:
    @staticmethod
    def create_order(username, data):
        product_id = data.get('product')
        
        user = MongoService.find_one('users', {"username": username})
        if not user:
            return {"status": "fail", "message": "User not found."}, 404

        # Normalize product_id to int
        try:
            p_id = int(product_id)
        except (ValueError, TypeError):
            return {"status": "fail", "message": "Invalid product ID"}, 400

        product = MongoService.find_one('products', {'id': p_id})
        if not product:
            return {"status": "fail", "message": "Product not found"}, 404
            
        orders = MongoService.find_all('orders')
        new_id = max([o.get('id', 0) for o in orders]) + 1 if orders else 1

        new_order = {
            "id": new_id,
            "user": username,
            "product": p_id,
            "product_name": product['name'],
            "price": product['price'] * int(data.get('quantity', 1)),
            "quantity": int(data.get('quantity', 1)),
            "date": str(datetime.date.today()),
            "paid": False
        }
        
        if MongoService.insert_one('orders', new_order):
            return {"status": "ok", "message": f"Order for {new_order['quantity']} item(s) placed!"}, 201
        return {"status": "fail", "message": "Error saving order"}, 500

    @staticmethod
    def get_user_orders(username):
        return MongoService.find_all('orders', {"user": username})

    @staticmethod
    def get_user_stats(username):
        user_orders = MongoService.find_all('orders', {"user": username})
        
        total_due = sum(o.get('price', 0) for o in user_orders if not o.get('paid', False))
        active_count = len([o for o in user_orders if not o.get('paid', False)])
        
        return {
            "total_due": total_due,
            "active_orders": active_count,
            "recent_activity": user_orders[-3:] if user_orders else []
        }

    @staticmethod
    def get_all_orders():
        return MongoService.find_all('orders')
