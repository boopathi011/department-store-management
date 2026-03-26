import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart-store-super-secret-key')
    DB_DIR = os.path.join(os.path.dirname(__file__), 'database')
    USERS_FILE = os.path.join(DB_DIR, 'users.json')
    PRODUCTS_FILE = os.path.join(DB_DIR, 'products.json')
    ORDERS_FILE = os.path.join(DB_DIR, 'orders.json')
    LOANS_FILE = os.path.join(DB_DIR, 'loans.json')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://user:password@cluster.mongodb.net/dbname')
    DATABASE_NAME = 'department_store'
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_placeholder')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'secret_placeholder')
    LOAN_REPAYMENT_DAYS = 4
