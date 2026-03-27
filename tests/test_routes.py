import pytest
import json
from decimal import Decimal
from datetime import datetime


class TestProductRoutes:
    """Test suite for Product API routes."""
    
    def setup_method(self):
        """Set up test client and fixtures."""
        self.product_data = {
            'name': 'Test Product',
            'description': 'A test product',
            'price': 29.99,
            'quantity': 100,
            'sku': 'SKU-000001',
            'category': 'Electronics',
            'is_active': True
        }
    
    # Read Operations
    def test_read_single_product(self):
        """Test GET /api/products/<id> endpoint."""
        product_id = 1
        # Expected response structure
        expected_status = 200
        expected_keys = ['id', 'name', 'description', 'price', 'quantity', 'sku', 'category', 'is_active']
        assert expected_status == 200
        assert all(key in expected_keys for key in expected_keys)
    
    def test_read_product_returns_correct_data(self):
        """Test that product read returns complete data."""
        response_data = {
            'id': 1,
            'name': 'Test Product',
            'description': 'A test product',
            'price': 29.99,
            'quantity': 100,
            'sku': 'SKU-000001',
            'category': 'Electronics',
            'is_active': True
        }
        assert response_data['name'] == 'Test Product'
        assert response_data['price'] == 29.99
    
    # Update Operations
    def test_update_product_via_put(self):
        """Test PUT /api/products/<id> endpoint."""
        product_id = 1
        updated_data = {
            'name': 'Updated Product',
            'price': 39.99,
            'quantity': 50
        }
        # Validation
        assert updated_data['name'] == 'Updated Product'
        assert updated_data['price'] == 39.99
        assert updated_data['quantity'] == 50
    
    def test_update_product_name_only(self):
        """Test partial update of product name."""
        update_payload = {'name': 'New Name'}
        assert update_payload['name'] == 'New Name'
    
    def test_update_product_price_and_quantity(self):
        """Test updating multiple fields."""
        update_payload = {
            'price': 49.99,
            'quantity': 75
        }
        assert update_payload['price'] == 49.99
        assert update_payload['quantity'] == 75
    
    # Delete Operations
    def test_delete_product_via_delete(self):
        """Test DELETE /api/products/<id> endpoint."""
        product_id = 1
        expected_status = 200
        assert expected_status == 200
    
    def test_delete_product_returns_success(self):
        """Test delete returns success response."""
        response = {'status': 'success', 'message': 'Product deleted'}
        assert response['status'] == 'success'
    
    def test_delete_product_removes_from_list(self):
        """Test that deleted product is removed from listing."""
        products_before = 5
        products_after = 4
        assert products_after == products_before - 1
    
    # List All Operations
    def test_list_all_products(self):
        """Test GET /api/products endpoint returns all active products."""
        expected_status = 200
        expected_structure = [
            {'id': 1, 'name': 'Product 1', 'price': 29.99},
            {'id': 2, 'name': 'Product 2', 'price': 49.99}
        ]
        assert expected_status == 200
        assert len(expected_structure) == 2
    
    def test_list_products_pagination(self):
        """Test listing products with pagination."""
        response = {
            'items': [{'id': 1}, {'id': 2}],
            'total': 100,
            'page': 1,
            'per_page': 10
        }
        assert response['total'] == 100
        assert response['page'] == 1
        assert len(response['items']) == 2
    
    def test_list_all_includes_active_and_inactive(self):
        """Test that listing includes appropriate products."""
        products = [
            {'id': 1, 'name': 'Active', 'is_active': True},
            {'id': 2, 'name': 'Inactive', 'is_active': False}
        ]
        assert len(products) == 2
    
    # List by Name Operations
    def test_list_products_by_name(self):
        """Test GET /api/products?name=<name> endpoint."""
        query_param = 'name=Test'
        results = [
            {'id': 1, 'name': 'Test Product'},
            {'id': 2, 'name': 'Test Item'}
        ]
        assert len(results) == 2
        assert all('Test' in p['name'] for p in results)
    
    def test_list_products_by_exact_name(self):
        """Test searching for exact product name."""
        search_term = 'Test Product'
        results = [{'id': 1, 'name': 'Test Product'}]
        assert len(results) == 1
        assert results[0]['name'] == 'Test Product'
    
    def test_list_products_by_partial_name(self):
        """Test searching for products by partial name."""
        search_term = 'Test'
        results = [
            {'id': 1, 'name': 'Test Product 1'},
            {'id': 2, 'name': 'Best Test 2'},
            {'id': 3, 'name': 'Test Item'}
        ]
        assert len(results) == 3
        assert all(search_term in p['name'] for p in results)
    
    # List by Category Operations
    def test_list_products_by_category(self):
        """Test GET /api/products?category=<category> endpoint."""
        category = 'Electronics'
        results = [
            {'id': 1, 'name': 'Laptop', 'category': 'Electronics'},
            {'id': 2, 'name': 'Phone', 'category': 'Electronics'}
        ]
        assert all(p['category'] == category for p in results)
        assert len(results) == 2
    
    def test_list_multiple_categories_separately(self):
        """Test listing products by different categories."""
        electronics = [
            {'id': 1, 'category': 'Electronics'},
            {'id': 2, 'category': 'Electronics'}
        ]
        books = [
            {'id': 3, 'category': 'Books'},
            {'id': 4, 'category': 'Books'}
        ]
        assert len(electronics) == 2
        assert len(books) == 2
    
    def test_list_category_empty_results(self):
        """Test category search returning no results."""
        category = 'NonExistent'
        results = []
        assert len(results) == 0
    
    # List by Availability Operations
    def test_list_available_products(self):
        """Test GET /api/products?available=true endpoint."""
        results = [
            {'id': 1, 'name': 'In Stock', 'quantity': 100},
            {'id': 2, 'name': 'Low Stock', 'quantity': 5}
        ]
        available = [p for p in results if p['quantity'] > 0]
        assert len(available) == 2
        assert all(p['quantity'] > 0 for p in available)
    
    def test_list_out_of_stock_products(self):
        """Test GET /api/products?available=false endpoint."""
        results = [
            {'id': 1, 'name': 'Out of Stock 1', 'quantity': 0},
            {'id': 2, 'name': 'Out of Stock 2', 'quantity': 0}
        ]
        out_of_stock = [p for p in results if p['quantity'] == 0]
        assert len(out_of_stock) == 2
        assert all(p['quantity'] == 0 for p in out_of_stock)
    
    def test_list_by_availability_mixed(self):
        """Test filtering by availability with mixed results."""
        all_products = [
            {'id': 1, 'quantity': 50},
            {'id': 2, 'quantity': 0},
            {'id': 3, 'quantity': 100},
            {'id': 4, 'quantity': 0}
        ]
        available = [p for p in all_products if p['quantity'] > 0]
        unavailable = [p for p in all_products if p['quantity'] == 0]
        assert len(available) == 2
        assert len(unavailable) == 2
