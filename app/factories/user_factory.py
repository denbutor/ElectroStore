from random import random, randint
from app.db.schemas.user import UserCreate


class UserFactory:
    @staticmethod
    def create_sample_user() -> UserCreate:
        return UserCreate(
            email=f"user{randint(1, 1000)}@example.com",
            password="securepassword",
            name="Test",
            surname="User",
            phone_number="+380123456789",
            city="Kyiv" ,
            nova_post_department="1",
        )