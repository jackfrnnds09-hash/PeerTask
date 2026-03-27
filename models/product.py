"""
Product model for the application.
"""
from datetime import datetime
from decimal import Decimal


class Product:
    """Product model class."""
    
    def __init__(self, id=None, name='', description='', price=0.0, quantity=0,
                 sku='', category='', is_active=True, created_at=None, updated_at=None):
        """Initialize a Product instance."""
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.sku = sku
        self.category = category
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def __repr__(self):
        """String representation of Product."""
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"
    
    def to_dict(self):
        """Convert Product to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'quantity': self.quantity,
            'sku': self.sku,
            'category': self.category,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
