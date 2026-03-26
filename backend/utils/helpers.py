import datetime

def format_currency(amount):
    return f"₹{amount:,.2f}"

def get_deadline(order_date_str, days=4):
    order_date = datetime.date.fromisoformat(order_date_str)
    return str(order_date + datetime.timedelta(days=days))
