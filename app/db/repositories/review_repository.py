from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.review import Review
from app.db.repositories.ireview_repository import IReviewRepository
from app.db.schemas.review import ReviewUpdate


class ReviewRepository(IReviewRepository):
    async def create_review(self, db: AsyncSession, review: Review) -> Review:
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return review

    async def get_by_user_and_product(self, db: AsyncSession, user_id: int, product_id: int) -> Review | None:
        result = await db.execute(
            select(Review).where(Review.user_id == user_id, Review.product_id == product_id)
        )
        return result.scalars().first()

    async def get_reviews_by_product(self, db: AsyncSession, product_id: int) -> list[Review]:
        result = await db.execute(select(Review).where(Review.product_id == product_id))
        return result.scalars().all()

    async def get_reviews_by_user(self, db: AsyncSession, user_id: int) -> list[Review]:
        result = await db.execute(select(Review).where(Review.user_id == user_id))
        return result.scalars().all()

    async def update_review(self, db: AsyncSession, review: Review, data: ReviewUpdate) -> Review:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(review, field, value)
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return review

    async def delete_review(self, db: AsyncSession, review: Review):
        await db.delete(review)
        await db.commit()