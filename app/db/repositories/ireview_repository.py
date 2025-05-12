from abc import abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.review import Review
from app.db.schemas.review import ReviewUpdate


class IReviewRepository:
    @abstractmethod
    async def create_review(self, db: AsyncSession, review: Review) -> Review:
        pass

    @abstractmethod
    async def get_reviews_by_product(self, db: AsyncSession, product_id: int) -> list[Review]:
        pass

    @abstractmethod
    async def get_reviews_by_user(self, db: AsyncSession, user_id: int) -> list[Review]:
        pass

    @abstractmethod
    async def get_by_user_and_product(self, db: AsyncSession, user_id: int, product_id: int) -> Review | None:
        pass

    @abstractmethod
    async def delete_review(self, db: AsyncSession, review: Review):
        pass

    @abstractmethod
    async def update_review(self, db: AsyncSession, review: Review, data: ReviewUpdate) -> Review:
        pass
