import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '6323c147614338cb639a0b0e147703ae8255a12a428a6fb2a815227fb9e8218da')
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '6323c147614338cb639a0b0e147703ae8255a12a428a6fb2a815227fb9e8218da')
    DB_DIR = os.path.join(os.path.dirname(__file__), 'database')
    USERS_FILE = os.path.join(DB_DIR, 'users.json')
    PRODUCTS_FILE = os.path.join(DB_DIR, 'products.json')
    ORDERS_FILE = os.path.join(DB_DIR, 'orders.json')
    LOANS_FILE = os.path.join(DB_DIR, 'loans.json')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://Onlinestore:boopathi2005@cluster0.9pnebvb.mongodb.net/?appName=Cluster0')
    DATABASE_NAME = 'department_store'
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_SNnWHNB76cgJxI')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'kmRCNgF1d5gQ0K3ds7xS8x7P')
    LOAN_REPAYMENT_DAYS = 4