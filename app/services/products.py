from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product
from app.db.repositories.product_repository import ProductRepository
from app.db.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.db.schemas.user import UserResponse
from app.decorators.admin_decorator import requires_admin
from app.exceptions import ForbiddenException


class ProductService:
# -----------------------------------------------------------------------
#Fisrt Version!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#------------------------------------------------------------------------
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo
#------------------------------------------------------------------------

# -----------------------------------------------------------------------
#Fisrt GPT Version!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#------------------------------------------------------------------------
    # def __init__(self, product_repo: ProductRepository, db: AsyncSession):
    #     self.product_repo = product_repo
    #     self.db = db
#------------------------------------------------------------------------

    # @requires_admin
    async def create_product(
            self, db: AsyncSession,
            product_data: ProductCreate,
            current_user: UserResponse,
    ) -> ProductResponse:
        if current_user.role != "admin":
            raise ForbiddenException(detail="Insufficient privileges")
        new_product = await self.product_repo.create_product(db, product_data)
        return ProductResponse.model_validate(new_product)

    async def get_products(self, db: AsyncSession):
        return await self.product_repo.get_products(db)

    async def get_product_by_name(self, db: AsyncSession, name: str) -> ProductResponse | None:
        product = await self.product_repo.get_product_by_name(db, name)
        if not product:
            return None
        return ProductResponse.model_validate(product)

    async def search_products_by_name(self, db: AsyncSession, name: str) -> list[ProductResponse]:
        products = await self.product_repo.search_products_by_name(db, name)
        return [ProductResponse.model_validate(product) for product in products]

    @requires_admin
    async def update_product(self, db: AsyncSession, product_id: int, updated_data: ProductUpdate) -> ProductResponse:
        product = await self.product_repo.update_product(db, product_id, updated_data)
        return ProductResponse.model_validate(product)

    @requires_admin
    async def delete_product(self, db: AsyncSession, product_id: int):
        await self.product_repo.delete_product(db, product_id)
