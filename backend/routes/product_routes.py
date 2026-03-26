from flask import Blueprint, request, jsonify
from controllers.product_controller import ProductController
from utils.auth_middleware import token_required, admin_required

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    result, status = ProductController.get_all()
    return jsonify(result), status

@product_bp.route('/add_product', methods=['POST'])
@token_required
@admin_required
def add_product(current_user, role):
    # Support both JSON and multipart/form-data
    if request.is_json:
        data = request.json
        file = None
    else:
        data = request.form.to_dict()
        file = request.files.get('image')
        
    result, status = ProductController.add_product(data, file)
    return jsonify(result), status
@product_bp.route('/update_product/<int:product_id>', methods=['POST'])
@token_required
@admin_required
def update_product(current_user, role, product_id):
    if request.is_json:
        data = request.json
        file = None
    else:
        data = request.form.to_dict()
        file = request.files.get('image')
        
    result, status = ProductController.update_product(product_id, data, file)
    return jsonify(result), status
