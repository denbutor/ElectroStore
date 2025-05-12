from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.review import ReviewUpdate, ReviewOut, ReviewCreate
from app.services.review import ReviewService
from app.db.repositories.review_repository import ReviewRepository
from app.db.schemas import review as schema
from app.core.security import get_db, get_current_user

router = APIRouter()

# review_repo = ReviewRepository()


review_service = ReviewService(ReviewRepository())

@router.post("/", response_model=ReviewOut)
async def create_review(
    data: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        return await review_service.create_review(db, user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/product/{product_id}", response_model=list[ReviewOut])
async def get_product_reviews(product_id: int, db: AsyncSession = Depends(get_db)):
    return await review_service.get_reviews_by_product(db, product_id)

@router.get("/my", response_model=list[ReviewOut])
async def get_my_reviews(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    return await review_service.get_reviews_by_user(db, user.id)

@router.put("/", response_model=ReviewOut)
async def update_review(
    data: ReviewUpdate,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        return await review_service.update_review(db, user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/product/{product_id}")
async def delete_review(
        product_id: int,
        db: AsyncSession = Depends(get_db),
        user = Depends(get_current_user)
):
    try:
        await review_service.delete_review(db, user.id, product_id)
        return { "detail": "Review deleted successfully" }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))