import factory
from decimal import Decimal
from datetime import datetime


class ProductFactory(factory.Factory):
    """Factory for creating fake Product instances for testing."""
    
    class Meta:
        model = 'products.Product'
    
    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('word')
    description = factory.Faker('text', max_nb_chars=200)
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    quantity = factory.Faker('random_int', min=0, max=1000)
    sku = factory.Sequence(lambda n: f'SKU-{n:06d}')
    category = factory.Faker('word')
    is_active = True
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')


class ProductBatchFactory(factory.DjangoModelFactory):
    """Factory for batch creating multiple fake products."""
    
    class Meta:
        model = 'products.Product'
    
    @classmethod
    def create_batch(cls, size=10):
        """Create multiple fake products at once."""
        return [ProductFactory() for _ in range(size)]
