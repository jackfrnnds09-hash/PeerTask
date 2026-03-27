"""
Product service routes - API endpoints for product management.
"""
from flask import Blueprint, request, jsonify
from decimal import Decimal
from datetime import datetime

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

# In-memory storage for products (in production, use database)
products_db = {}
product_id_counter = 1


@products_bp.route('/<int:product_id>', methods=['GET'])
def read_product(product_id):
    """
    Read a single product by ID.
    GET /api/products/<id>
    """
    if product_id not in products_db:
        return jsonify({'error': 'Product not found'}), 404
    
    product = products_db[product_id]
    return jsonify(product), 200


@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Update a product by ID.
    PUT /api/products/<id>
    """
    if product_id not in products_db:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    product = products_db[product_id]
    
    # Update allowed fields
    if 'name' in data:
        product['name'] = data['name']
    if 'description' in data:
        product['description'] = data['description']
    if 'price' in data:
        product['price'] = float(data['price'])
    if 'quantity' in data:
        product['quantity'] = data['quantity']
    if 'category' in data:
        product['category'] = data['category']
    if 'is_active' in data:
        product['is_active'] = data['is_active']
    
    product['updated_at'] = datetime.now().isoformat()
    products_db[product_id] = product
    
    return jsonify(product), 200


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Delete a product by ID.
    DELETE /api/products/<id>
    """
    if product_id not in products_db:
        return jsonify({'error': 'Product not found'}), 404
    
    del products_db[product_id]
    return jsonify({'status': 'success', 'message': 'Product deleted'}), 200


@products_bp.route('', methods=['GET'])
def list_all_products():
    """
    List all products with optional filtering.
    GET /api/products
    """
    products = list(products_db.values())
    return jsonify(products), 200


@products_bp.route('/search/name', methods=['GET'])
def list_products_by_name():
    """
    List products by name search.
    GET /api/products/search/name?q=<search_term>
    """
    search_term = request.args.get('q', '').lower()
    
    if not search_term:
        return jsonify({'error': 'Search term required'}), 400
    
    results = [
        p for p in products_db.values()
        if search_term in p.get('name', '').lower()
    ]
    
    return jsonify(results), 200


@products_bp.route('/search/category', methods=['GET'])
def list_products_by_category():
    """
    List products by category.
    GET /api/products/search/category?category=<category>
    """
    category = request.args.get('category', '').lower()
    
    if not category:
        return jsonify({'error': 'Category required'}), 400
    
    results = [
        p for p in products_db.values()
        if p.get('category', '').lower() == category
    ]
    
    return jsonify(results), 200


@products_bp.route('/search/availability', methods=['GET'])
def list_products_by_availability():
    """
    List products by availability (in stock or not).
    GET /api/products/search/availability?available=<true|false>
    """
    available_param = request.args.get('available', '').lower()
    
    if available_param not in ['true', 'false']:
        return jsonify({'error': 'Available parameter must be true or false'}), 400
    
    available = available_param == 'true'
    
    if available:
        results = [p for p in products_db.values() if p.get('quantity', 0) > 0]
    else:
        results = [p for p in products_db.values() if p.get('quantity', 0) == 0]
    
    return jsonify(results), 200


@products_bp.route('', methods=['POST'])
def create_product():
    """
    Create a new product.
    POST /api/products
    """
    global product_id_counter
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'price', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_product = {
        'id': product_id_counter,
        'name': data['name'],
        'description': data.get('description', ''),
        'price': float(data['price']),
        'quantity': data.get('quantity', 0),
        'sku': data.get('sku', f'SKU-{product_id_counter:06d}'),
        'category': data['category'],
        'is_active': data.get('is_active', True),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    products_db[product_id_counter] = new_product
    product_id_counter += 1
    
    return jsonify(new_product), 201


@products_bp.route('/filter', methods=['GET'])
def filter_products():
    """
    Advanced filtering for products.
    GET /api/products/filter?name=<name>&category=<category>&available=<true|false>
    """
    name_filter = request.args.get('name', '').lower()
    category_filter = request.args.get('category', '').lower()
    available_filter = request.args.get('available', '').lower()
    
    results = list(products_db.values())
    
    if name_filter:
        results = [p for p in results if name_filter in p.get('name', '').lower()]
    
    if category_filter:
        results = [p for p in results if p.get('category', '').lower() == category_filter]
    
    if available_filter in ['true', 'false']:
        available = available_filter == 'true'
        if available:
            results = [p for p in results if p.get('quantity', 0) > 0]
        else:
            results = [p for p in results if p.get('quantity', 0) == 0]
    
    return jsonify(results), 200


@products_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


@products_bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    return jsonify({'error': 'Bad request'}), 400
