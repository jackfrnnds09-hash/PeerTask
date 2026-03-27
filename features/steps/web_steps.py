"""
Web steps for BDD testing - step definitions for feature scenarios.
"""
from behave import when, then
import requests
import json


@when('I request to read the product with ID {product_id:d}')
def read_product_step(context, product_id):
    """
    Read a product by ID via API.
    """
    url = f"{context.api_url}/api/products/{product_id}"
    context.response = requests.get(url)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = None


@when('I update the product with:')
def update_product_step(context):
    """
    Update a product via API.
    
    Example:
        When I update the product with:
            | name  | Updated Name |
            | price | 199.99       |
    """
    product_id = getattr(context, 'product_id', 1)
    url = f"{context.api_url}/api/products/{product_id}"
    
    update_data = {}
    for row in context.table:
        key = row[0]
        value = row[1]
        
        if key == 'price':
            update_data[key] = float(value)
        elif key == 'quantity':
            update_data[key] = int(value)
        else:
            update_data[key] = value
    
    context.response = requests.put(url, json=update_data)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = None


@when('I delete the product with ID {product_id:d}')
def delete_product_step(context, product_id):
    """
    Delete a product via API.
    """
    url = f"{context.api_url}/api/products/{product_id}"
    context.response = requests.delete(url)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = None


@when('I request to list all products')
def list_all_products_step(context):
    """
    List all products via API.
    """
    url = f"{context.api_url}/api/products"
    context.response = requests.get(url)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = []


@when('I search for products with name "{search_term}"')
def search_by_name_step(context, search_term):
    """
    Search for products by name.
    """
    url = f"{context.api_url}/api/products/search/name"
    params = {'q': search_term}
    context.response = requests.get(url, params=params)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = []


@when('I search for products with exact name "{search_term}"')
def search_by_exact_name_step(context, search_term):
    """
    Search for products by exact name.
    """
    url = f"{context.api_url}/api/products/search/name"
    params = {'q': search_term, 'exact': 'true'}
    context.response = requests.get(url, params=params)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = []


@when('I search for products in category "{category}"')
def search_by_category_step(context, category):
    """
    Search for products by category.
    """
    url = f"{context.api_url}/api/products/search/category"
    params = {'category': category}
    context.response = requests.get(url, params=params)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = []


@when('I search for available products')
def search_available_products_step(context):
    """
    Search for available (in-stock) products.
    """
    url = f"{context.api_url}/api/products/search/availability"
    params = {'available': 'true'}
    context.response = requests.get(url, params=params)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = []


@when('I search for unavailable products')
def search_unavailable_products_step(context):
    """
    Search for unavailable (out-of-stock) products.
    """
    url = f"{context.api_url}/api/products/search/availability"
    params = {'available': 'false'}
    context.response = requests.get(url, params=params)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = []


@when('I filter for products by availability "{availability}"')
def filter_by_availability_step(context, availability):
    """
    Filter products by availability status.
    """
    url = f"{context.api_url}/api/products/search/availability"
    available_value = 'true' if availability.lower() == 'available' else 'false'
    params = {'available': available_value}
    context.response = requests.get(url, params=params)
    
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = []


@then('the response status should be {status_code:d}')
def check_response_status(context, status_code):
    """
    Verify the HTTP response status code.
    """
    assert context.response.status_code == status_code, \
        f"Expected status {status_code}, got {context.response.status_code}"


@then('the product name should be "{expected_name}"')
def check_product_name(context, expected_name):
    """
    Verify the product name in the response.
    """
    assert context.response_data['name'] == expected_name, \
        f"Expected name '{expected_name}', got '{context.response_data.get('name')}'"


@then('the product price should be {expected_price:f}')
def check_product_price(context, expected_price):
    """
    Verify the product price in the response.
    """
    assert float(context.response_data['price']) == expected_price, \
        f"Expected price {expected_price}, got {context.response_data.get('price')}"


@then('the product category should be "{expected_category}"')
def check_product_category(context, expected_category):
    """
    Verify the product category in the response.
    """
    assert context.response_data['category'] == expected_category, \
        f"Expected category '{expected_category}', got '{context.response_data.get('category')}'"


@then('the product quantity should be {expected_quantity:d}')
def check_product_quantity(context, expected_quantity):
    """
    Verify the product quantity in the response.
    """
    assert context.response_data['quantity'] == expected_quantity, \
        f"Expected quantity {expected_quantity}, got {context.response_data.get('quantity')}"


@then('the product with ID {product_id:d} should not exist')
def check_product_not_exists(context, product_id):
    """
    Verify that a product does not exist.
    """
    url = f"{context.api_url}/api/products/{product_id}"
    response = requests.get(url)
    assert response.status_code == 404, \
        f"Expected product to be deleted (404), got {response.status_code}"


@then('the products list should contain {expected_count:d} items')
def check_products_list_count(context, expected_count):
    """
    Verify the number of products in the list.
    """
    assert len(context.response_data) == expected_count, \
        f"Expected {expected_count} products, got {len(context.response_data)}"


@then('the product list should include "{product_name}"')
def check_product_in_list(context, product_name):
    """
    Verify that a product is in the list.
    """
    product_names = [p.get('name') for p in context.response_data]
    assert product_name in product_names, \
        f"Product '{product_name}' not found in list: {product_names}"


@then('the search results should contain {expected_count:d} products')
def check_search_results_count(context, expected_count):
    """
    Verify the number of search results.
    """
    assert len(context.response_data) == expected_count, \
        f"Expected {expected_count} results, got {len(context.response_data)}"


@then('the results should include "{product_name}"')
def check_result_includes(context, product_name):
    """
    Verify that search results include a specific product.
    """
    product_names = [p.get('name') for p in context.response_data]
    assert product_name in product_names, \
        f"Product '{product_name}' not found in results: {product_names}"


@then('the results should not include "{product_name}"')
def check_result_not_includes(context, product_name):
    """
    Verify that search results do not include a specific product.
    """
    product_names = [p.get('name') for p in context.response_data]
    assert product_name not in product_names, \
        f"Product '{product_name}' should not be in results: {product_names}"


@then('all results should have category "{expected_category}"')
def check_all_results_category(context, expected_category):
    """
    Verify that all results have the same category.
    """
    for product in context.response_data:
        assert product.get('category') == expected_category, \
            f"Product '{product.get('name')}' has category '{product.get('category')}', " \
            f"expected '{expected_category}'"


@then('the result should have name "{expected_name}"')
def check_result_name(context, expected_name):
    """
    Verify the name of a single result.
    """
    assert context.response_data[0]['name'] == expected_name, \
        f"Expected name '{expected_name}', got '{context.response_data[0].get('name')}'"


@then('all results should have quantity greater than {threshold:d}')
def check_all_results_quantity_greater(context, threshold):
    """
    Verify that all results have quantity greater than threshold.
    """
    for product in context.response_data:
        assert product.get('quantity', 0) > threshold, \
            f"Product '{product.get('name')}' has quantity {product.get('quantity')}, " \
            f"expected > {threshold}"


@then('all results should have quantity equal to {expected_quantity:d}')
def check_all_results_quantity_equal(context, expected_quantity):
    """
    Verify that all results have equal quantity.
    """
    for product in context.response_data:
        assert product.get('quantity') == expected_quantity, \
            f"Product '{product.get('name')}' has quantity {product.get('quantity')}, " \
            f"expected {expected_quantity}"
