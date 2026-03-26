from database.mongo_service import MongoService
from config import Config
import os

class ProductController:
    @staticmethod
    def get_all():
        return MongoService.find_all('products')

    @staticmethod
    def add_product(data, file=None):
        name = data.get('name')
        price = data.get('price')
        category = data.get('category')

        if not name or not price or not category:
            return {"status": "fail", "message": "Missing required fields (name, price, category)"}, 400
            
        products = MongoService.find_all('products')
        new_id = max([p.get('id', 0) for p in products]) + 1 if products else 1
        
        image_url = data.get('image', 'https://placehold.co/400x300?text=📦')
        
        if file:
            try:
                import werkzeug.utils
                filename = werkzeug.utils.secure_filename(f"product_{new_id}_{file.filename}")
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                file.save(filepath)
                image_url = f"/api/uploads/{filename}"
            except Exception as e:
                print(f"Upload failed: {str(e)}. Defaulting to URL.")
                # On Vercel, this might fail, so we fallback to the URL if provided
                image_url = data.get('image', 'https://placehold.co/400x300?text=📦')

        new_product = {
            "id": new_id,
            "name": name,
            "price": float(price),
            "category": category,
            "image": image_url
        }
        
        if MongoService.insert_one('products', new_product):
            return {"status": "ok", "message": "Product added", "id": new_id}, 201
        return {"status": "fail", "message": "Error saving product"}, 500

    @staticmethod
    def update_product(product_id, data, file=None):
        product = MongoService.find_one('products', {'id': int(product_id)})
        
        if not product:
            return {"status": "fail", "message": "Product not found"}, 404
            
        update_data = {}
        if 'name' in data: update_data['name'] = data['name']
        if 'price' in data: update_data['price'] = float(data['price'])
        if 'category' in data: update_data['category'] = data['category']
        
        if file:
            import werkzeug.utils
            filename = werkzeug.utils.secure_filename(f"product_{product_id}_{file.filename}")
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            update_data['image'] = f"/uploads/{filename}"
        elif 'image' in data:
             update_data['image'] = data['image']

        if MongoService.update_one('products', {'id': int(product_id)}, update_data):
            return {"status": "ok", "message": "Product updated"}, 200
        return {"status": "fail", "message": "Error updating product"}, 500
