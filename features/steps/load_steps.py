"""
Load steps for BDD testing - loads test data for feature scenarios.
"""
from behave import given
import json
import os


@given('I have the following products')
def load_products(context):
    """
    Load products from the feature file table.
    
    Example:
        Given I have the following products:
            | name         | description      | price | quantity | category    |
            | Laptop       | Portable computer| 999.99| 10       | Electronics |
            | Book         | Programming 101 | 29.99 | 50       | Books       |
    """
    context.products = []
    
    for row in context.table:
        product = {
            'id': len(context.products) + 1,
            'name': row['name'],
            'description': row['description'],
            'price': float(row['price']),
            'quantity': int(row['quantity']),
            'category': row['category'],
            'sku': f"SKU-{len(context.products) + 1:06d}",
            'is_active': True
        }
        context.products.append(product)


@given('a product in the database with details')
def load_single_product(context):
    """
    Load a single product for testing.
    
    Example:
        Given a product in the database with details:
            | name        | Test Product      |
            | description | A test product    |
            | price       | 29.99            |
            | quantity    | 100              |
            | category    | Electronics      |
    """
    context.product = {}
    
    for row in context.table:
        key = row[0]
        value = row[1]
        
        if key == 'price':
            context.product[key] = float(value)
        elif key == 'quantity':
            context.product[key] = int(value)
        else:
            context.product[key] = value
    
    context.product['id'] = 1
    context.product['sku'] = 'SKU-000001'
    context.product['is_active'] = True


@given('the database is empty')
def clear_database(context):
    """Clear all data from the database."""
    context.products = []
    context.product = None


@given('a list of {count:d} products')
def load_multiple_products(context, count):
    """Load multiple products for bulk operations."""
    context.products = []
    
    for i in range(1, count + 1):
        product = {
            'id': i,
            'name': f'Product {i}',
            'description': f'Description for product {i}',
            'price': 10.00 + (i * 5),
            'quantity': 10 * i,
            'category': 'General' if i % 2 == 0 else 'Electronics',
            'sku': f'SKU-{i:06d}',
            'is_active': True
        }
        context.products.append(product)


@given('products by name')
def load_products_by_name(context):
    """
    Load products organized by name for searching.
    
    Example:
        Given products by name:
            | name           | quantity |
            | Laptop Pro     | 5        |
            | Laptop Basic   | 10       |
            | Mouse          | 100      |
    """
    context.products_by_name = {}
    
    for row in context.table:
        name = row['name']
        quantity = int(row['quantity'])
        context.products_by_name[name] = {
            'name': name,
            'quantity': quantity,
            'category': 'Electronics'
        }


@given('products by category')
def load_products_by_category(context):
    """
    Load products organized by category.
    
    Example:
        Given products by category:
            | category    | name    | quantity |
            | Electronics | Laptop  | 5        |
            | Electronics | Phone   | 20       |
            | Books       | Python  | 50       |
            | Books       | Java    | 30       |
    """
    context.products_by_category = {}
    
    for row in context.table:
        category = row['category']
        if category not in context.products_by_category:
            context.products_by_category[category] = []
        
        product = {
            'name': row['name'],
            'quantity': int(row['quantity']),
            'category': category
        }
        context.products_by_category[category].append(product)


@given('products with availability')
def load_products_with_availability(context):
    """
    Load products with varying availability.
    
    Example:
        Given products with availability:
            | name     | quantity | available |
            | Product1 | 100      | true      |
            | Product2 | 0        | false     |
            | Product3 | 5        | true      |
    """
    context.products_availability = []
    
    for row in context.table:
        product = {
            'name': row['name'],
            'quantity': int(row['quantity']),
            'available': row['available'].lower() == 'true'
        }
        context.products_availability.append(product)


@given('I initialize the test environment')
def initialize_environment(context):
    """Initialize the test environment with default values."""
    context.api_url = os.environ.get('API_URL', 'http://localhost:5000')
    context.response = None
    context.response_data = None
    context.error = None
    context.products = []
