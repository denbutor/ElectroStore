from app.db.models.product import Product
from app.db.repositories.icart_repository import ICartRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from app.db.models.cart import Cart
from app.db.models.cart_item import CartItem

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.exceptions import ProductNotFoundException, CartItemNotFoundException, CartNotFoundException


# from schemas import CartCreate, CartUpdate
class CartRepository(ICartRepository):
    async def get_cart_by_user_id(self, user_id: int, db: AsyncSession) -> Cart | None:
        """Отримати кошик користувача разом із товарами та продуктами"""
        result = await db.execute(
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(selectinload(Cart.cart_items).selectinload(CartItem.product))  # ✅ завантажує cart_items + product
        )
        return result.scalars().first()

    async def create_cart(self, user_id: int, db: AsyncSession) -> Cart:
        """Створити кошик для користувача"""
        new_cart = Cart(user_id=user_id)
        db.add(new_cart)
        await db.commit()
        await db.refresh(new_cart)
        return new_cart

    async def add_to_cart(self, db: AsyncSession, user_id: int, product_id: int, quantity: int) -> CartItem:
        cart = await self.get_cart_by_user_id(user_id, db)
        if not cart:
            cart = await self.create_cart(user_id, db)

        product = await db.get(Product, product_id)
        if not product:
            raise ProductNotFoundException()

        result = await db.execute(
            select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
        )
        cart_item = result.scalars().first()

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity, sum_price=0)
            db.add(cart_item)

        await db.commit()

        # 🔥 Підвантажуємо з selectinload, щоб мати cart_item.product
        result = await db.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.id == cart_item.id)
        )
        return result.scalars().first()

    async def remove_from_cart(self, db: AsyncSession, user_id: int, product_id: int) -> bool:
        """Видалити товар з кошика"""
        cart = await self.get_cart_by_user_id(user_id, db)
        if not cart:
            raise ProductNotFoundException()

        result = await db.execute(
            select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
        )
        cart_item = result.scalars().first()

        if not cart_item:
            raise CartItemNotFoundException()

        await db.delete(cart_item)
        await db.commit()
        return True

    async def clear_cart(self, db: AsyncSession, user_id: int) -> bool:
        """Очистити кошик користувача"""
        cart = await self.get_cart_by_user_id(user_id, db)
        if not cart:
            raise CartNotFoundException()

        await db.execute(
            CartItem.__table__.delete().where(CartItem.cart_id == cart.id)
        )
        await db.commit()
        return True
