from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from config import Config
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.admin_routes import admin_bp
from routes.loan_routes import loan_bp
from routes.analytics_routes import analytics_bp
from routes.payment_routes import payment_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Register Blueprints with /api prefix
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(loan_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')

@app.route('/api/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    app.run(debug=True, port=5555)
