from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.product_repository import ProductRepository
from app.db.schemas.product import ProductCreate
from app.decorators.admin_decorator import requires_admin


class ProductService:
# -----------------------------------------------------------------------
#Fisrt Version!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#------------------------------------------------------------------------
    # def __init__(self, product_repo: ProductRepository):
    #     self.product_repo = product_repo
#------------------------------------------------------------------------

# -----------------------------------------------------------------------
#Fisrt GPT Version!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#------------------------------------------------------------------------
    def __init__(self, product_repo: ProductRepository, db: AsyncSession):
        self.product_repo = product_repo
        self.db = db
#------------------------------------------------------------------------

    @requires_admin
    async def create(self, product_data: ProductCreate):
        return await self.product_repo.create_product(self.db, product_data)

    async def get_products(self, db: AsyncSession):
        return await self.product_repo.get_products(db)