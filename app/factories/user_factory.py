from random import random

from pip._internal.resolution.resolvelib import factory

from app.db.schemas.user import UserCreate


class UserFactory:
    @staticmethod
    def create_sample_user():
        return UserCreate(
            email= f"user {random.randint(1, 1000)}@example.com",
            password= "securepassword",
            full_name= "Test User",
        )