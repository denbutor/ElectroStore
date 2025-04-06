from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.review import Review
from app.db.repositories.review_repository import ReviewRepository
from app.db.schemas.review import ReviewCreate, ReviewUpdate


class ReviewService:
    def __init__(self, repository: ReviewRepository):
        self.repository = repository

    async def create_review(self, db: AsyncSession, user_id: int, data: ReviewCreate) -> Review:
        existing = await self.repository.get_by_user_and_product(db, user_id, data.product_id)
        if existing:
            raise ValueError("Review already exists")
        review = Review(**data.model_dump(), user_id=user_id)
        return await self.repository.create_review(db, review)

    async def get_reviews_by_product(self, db: AsyncSession, product_id: int) -> list[Review]:
        return await self.repository.get_reviews_by_product(db, product_id)

    async def get_reviews_by_user(self, db: AsyncSession, user_id: int) -> list[Review]:
        return await self.repository.get_reviews_by_user(db, user_id)

    async def update_review(self, db: AsyncSession, user_id: int, data: ReviewUpdate) -> Review:
        review = await self.repository.get_by_user_and_product(db, user_id, data.product_id)
        if not review:
            raise ValueError("Review not found")
        return await self.repository.update_review(db, review, data)

    async def delete_review(self, db: AsyncSession, user_id: int, product_id: int):
        review = await self.repository.get_by_user_and_product(db, user_id, product_id)
        if not review:
            raise ValueError("Review not found")
        await self.repository.delete_review(db, review)
