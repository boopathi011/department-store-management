import datetime
from database.mongo_service import MongoService
from config import Config

class ReminderService:
    @staticmethod
    def get_pending_reminders():
        orders = MongoService.find_all('orders', {"paid": False})
        today = datetime.date.today()
        due_soon = []
        
        for o in orders:
            order_date = datetime.date.fromisoformat(o['date'])
            deadline = o.get('deadline_days', Config.LOAN_REPAYMENT_DAYS)
            days_passed = (today - order_date).days
            days_remaining = deadline - days_passed
            
            if days_remaining <= 1: # 1 day before or overdue
                due_soon.append({
                    "id": o['id'],
                    "user": o['user'],
                    "message": f"Payment for {o['product_name']} is due in {days_remaining} days." if days_remaining >= 0 else f"Payment for {o['product_name']} is OVERDUE.",
                    "critical": days_remaining <= 0,
                    "reminder_sent_at": o.get('reminder_sent_at')
                })
        return due_soon
