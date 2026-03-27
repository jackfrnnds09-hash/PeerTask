import pytest
from datetime import datetime
from decimal import Decimal
from models.product import Product


class TestProductModel:
    """Test suite for Product model operations."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.product_data = {
            'id': 1,
            'name': 'Test Product',
            'description': 'A test product',
            'price': Decimal('29.99'),
            'quantity': 100,
            'sku': 'SKU-000001',
            'category': 'Electronics',
            'is_active': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
    
    # Read Operations
    def test_read_product_by_id(self):
        """Test reading a product by ID."""
        product = Product(**self.product_data)
        assert product.id == 1
        assert product.name == 'Test Product'
        assert product.price == Decimal('29.99')
    
    def test_read_product_attributes(self):
        """Test reading all attributes of a product."""
        product = Product(**self.product_data)
        assert product.description == 'A test product'
        assert product.quantity == 100
        assert product.sku == 'SKU-000001'
        assert product.category == 'Electronics'
        assert product.is_active is True
    
    # Update Operations
    def test_update_product_name(self):
        """Test updating a product's name."""
        product = Product(**self.product_data)
        product.name = 'Updated Product'
        assert product.name == 'Updated Product'
    
    def test_update_product_price(self):
        """Test updating a product's price."""
        product = Product(**self.product_data)
        product.price = Decimal('39.99')
        assert product.price == Decimal('39.99')
    
    def test_update_product_quantity(self):
        """Test updating product quantity."""
        product = Product(**self.product_data)
        product.quantity = 50
        assert product.quantity == 50
    
    def test_update_product_status(self):
        """Test updating product active status."""
        product = Product(**self.product_data)
        product.is_active = False
        assert product.is_active is False
    
    # Delete Operations
    def test_delete_product(self):
        """Test deleting a product."""
        product = Product(**self.product_data)
        product_id = product.id
        # Simulate delete by marking as inactive
        product.is_active = False
        assert product.is_active is False
        assert product.id == product_id
    
    def test_product_deletion_preserves_id(self):
        """Test that product ID is preserved after deletion."""
        product = Product(**self.product_data)
        original_id = product.id
        product.is_active = False
        assert product.id == original_id
    
    # List All Operations
    def test_list_all_products(self):
        """Test retrieving all products."""
        products = [
            Product(**self.product_data),
            Product(id=2, name='Product 2', description='Test 2', price=Decimal('49.99'),
                   quantity=50, sku='SKU-000002', category='Books', is_active=True,
                   created_at=datetime.now(), updated_at=datetime.now())
        ]
        assert len(products) == 2
        assert products[0].name == 'Test Product'
        assert products[1].name == 'Product 2'
    
    def test_list_active_products_only(self):
        """Test filtering active products."""
        products = [
            Product(**self.product_data),
            Product(id=2, name='Inactive Product', description='Test', price=Decimal('19.99'),
                   quantity=0, sku='SKU-000003', category='Other', is_active=False,
                   created_at=datetime.now(), updated_at=datetime.now())
        ]
        active_products = [p for p in products if p.is_active]
        assert len(active_products) == 1
        assert active_products[0].name == 'Test Product'
    
    # Find by Name Operations
    def test_find_product_by_name(self):
        """Test finding a product by name."""
        products = [
            Product(**self.product_data),
            Product(id=2, name='Another Product', description='Different', 
                   price=Decimal('19.99'), quantity=75, sku='SKU-000002', 
                   category='Books', is_active=True,
                   created_at=datetime.now(), updated_at=datetime.now())
        ]
        found = [p for p in products if p.name == 'Test Product']
        assert len(found) == 1
        assert found[0].id == 1
    
    def test_find_product_by_partial_name(self):
        """Test finding products by partial name match."""
        products = [
            Product(**self.product_data),
            Product(id=2, name='Test Item', description='Another test',
                   price=Decimal('15.99'), quantity=30, sku='SKU-000003',
                   category='Tools', is_active=True,
                   created_at=datetime.now(), updated_at=datetime.now())
        ]
        found = [p for p in products if 'Test' in p.name]
        assert len(found) == 2
    
    # Find by Category Operations
    def test_find_product_by_category(self):
        """Test finding products by category."""
        products = [
            Product(**self.product_data),
            Product(id=2, name='Electronics Item', description='Another',
                   price=Decimal('99.99'), quantity=20, sku='SKU-000004',
                   category='Electronics', is_active=True,
                   created_at=datetime.now(), updated_at=datetime.now()),
            Product(id=3, name='Book Item', description='Something',
                   price=Decimal('12.99'), quantity=100, sku='SKU-000005',
                   category='Books', is_active=True,
                   created_at=datetime.now(), updated_at=datetime.now())
        ]
        electronics = [p for p in products if p.category == 'Electronics']
        assert len(electronics) == 2
        assert all(p.category == 'Electronics' for p in electronics)
    
    def test_find_multiple_products_same_category(self):
        """Test finding multiple products in same category."""
        products = [
            Product(**self.product_data),
            Product(id=2, name='Item 2', description='Test',
                   price=Decimal('25.00'), quantity=40, sku='SKU-000006',
                   category='Electronics', is_active=True,
                   created_at=datetime.now(), updated_at=datetime.now())
        ]
        category_products = [p for p in products if p.category == 'Electronics']
        assert len(category_products) == 2
    
    # Find by Availability Operations
    def test_find_available_products(self):
        """Test finding available products (in stock)."""
        products = [
            Product(**self.product_data),
            Product(id=2, name='Out of Stock', description='None available',
                   price=Decimal('50.00'), quantity=0, sku='SKU-000007',
                   category='Electronics', is_active=True,
                   created_at=datetime.now(), updated_at=datetime.now())
        ]
        available = [p for p in products if p.quantity > 0]
        assert len(available) == 1
        assert available[0].quantity == 100
    
    def test_find_out_of_stock_products(self):
        """Test finding out of stock products."""
        products = [
            Product(**self.product_data),
            Product(id=2, name='Unavailable', description='Not in stock',
                   price=Decimal('30.00'), quantity=0, sku='SKU-000008',
                   category='Other', is_active=True,
                   created_at=datetime.now(), updated_at=datetime.now())
        ]
        out_of_stock = [p for p in products if p.quantity == 0]
        assert len(out_of_stock) == 1
        assert out_of_stock[0].name == 'Unavailable'
    
    def test_find_low_availability_products(self):
        """Test finding products with low availability."""
        products = [
            Product(**self.product_data),
            Product(id=2, name='Low Stock Item', description='Limited',
                   price=Decimal('15.99'), quantity=5, sku='SKU-000009',
                   category='Books', is_active=True,
                   created_at=datetime.now(), updated_at=datetime.now())
        ]
        low_stock = [p for p in products if 0 < p.quantity <= 10]
        assert len(low_stock) == 1
        assert low_stock[0].quantity == 5
