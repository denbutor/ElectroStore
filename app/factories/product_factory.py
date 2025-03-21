import random
from app.db.schemas.product import ProductCreate


class ProductFactory:
    @staticmethod
    def create_sample_product():
        return ProductCreate(
            name=f"Product {random.randint(1, 1000)}",
            description="Sample Product Description",
            price=random.condecimal(10, 500),
            category_id=random.randint(1, 5),
        )