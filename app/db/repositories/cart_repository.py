from app.db.models.product import Product
from app.db.repositories.icart_repository import ICartRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.models.cart import Cart
from app.db.models.cart_item import CartItem

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

# from schemas import CartCreate, CartUpdate
class CartRepository(ICartRepository):
    async def get_cart_by_user_id(self, user_id: int, db: AsyncSession) -> Cart | None:
        """Отримати кошик користувача"""
        result = await db.execute(select(Cart).where(Cart.user_id == user_id))
        return result.scalars().first()

    async def create_cart(self, user_id: int, db: AsyncSession) -> Cart:
        """Створити кошик для користувача"""
        new_cart = Cart(user_id=user_id)
        db.add(new_cart)
        await db.commit()
        await db.refresh(new_cart)
        return new_cart

    async def add_to_cart(self, db: AsyncSession, user_id: int, product_id: int, quantity: int) -> CartItem:
        """Додати товар у кошик"""
        cart = await self.get_cart_by_user_id(user_id, db)
        if not cart:
            cart = await self.create_cart(user_id, db)

        product = await db.get(Product, product_id)
        if not product:
            raise NoResultFound("Product not found")

        # Перевіряємо, чи товар вже є в кошику
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
        await db.refresh(cart_item)
        return cart_item

    async def remove_from_cart(self, db: AsyncSession, user_id: int, product_id: int) -> bool:
        """Видалити товар з кошика"""
        cart = await self.get_cart_by_user_id(user_id, db)
        if not cart:
            raise NoResultFound("Cart not found")

        result = await db.execute(
            select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
        )
        cart_item = result.scalars().first()

        if not cart_item:
            raise NoResultFound("Cart item not found")

        await db.delete(cart_item)
        await db.commit()
        return True

    async def clear_cart(self, db: AsyncSession, user_id: int) -> bool:
        """Очистити кошик користувача"""
        cart = await self.get_cart_by_user_id(user_id, db)
        if not cart:
            raise NoResultFound("Cart not found")

        await db.execute(
            CartItem.__table__.delete().where(CartItem.cart_id == cart.id)
        )
        await db.commit()
        return True

# class CartRepository(ICartRepository):
#     async def get_cart_by_user_id(self, user_id: int, db: AsyncSession) -> Cart | None:
#         """Отримати кошик користувача"""
#         result = await db.execute(select(Cart).where(Cart.user_id == user_id))
#         return result.scalars().first()
#
#     async def create_cart(self, user_id: int, db: AsyncSession) -> Cart:
#         """Створити кошик для користувача"""
#         new_cart = Cart(user_id=user_id)
#         db.add(new_cart)
#         await db.commit()
#         await db.refresh(new_cart)
#         return new_cart
#
#     async def add_to_cart(self, db: AsyncSession, user_id: int, product_id: int, quantity: int = 1) -> CartItem:
#         """Додати товар в кошик"""
#         cart = await self.get_cart_by_user_id(user_id, db)
#         if not cart:
#             cart = await self.create_cart(user_id, db)
#
#         result = await db.execute(select(Product).where(Product.id == product_id))
#         product = result.scalar_one_or_none()
#         if not product:
#             raise NoResultFound("Product not found")
#
#         # Перевіряємо, чи товар уже є в кошику
#         result = await db.execute(
#             select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
#         )
#         cart_item = result.scalar_one_or_none()
#
#         if cart_item:
#             cart_item.quantity += quantity
#         else:
#             cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
#             db.add(cart_item)
#
#         await db.commit()
#         await db.refresh(cart_item)
#         return cart_item
#
#     async def remove_from_cart(self, db: AsyncSession, user_id: int, product_id: int) -> bool:
#         """Видалити товар з кошика"""
#         cart = await self.get_cart_by_user_id(user_id, db)
#         if not cart:
#             raise NoResultFound("Cart not found")
#
#         result = await db.execute(
#             select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
#         )
#         cart_item = result.scalar_one_or_none()
#
#         if not cart_item:
#             raise NoResultFound("Cart item not found")
#
#         await db.delete(cart_item)
#         await db.commit()
#         return True
#
#     async def clear_cart(self, db: AsyncSession, user_id: int) -> bool:
#         """Очистити кошик користувача"""
#         cart = await self.get_cart_by_user_id(user_id, db)
#         if not cart:
#             raise NoResultFound("Cart not found")
#
#         await db.execute(
#             CartItem.__table__.delete().where(CartItem.cart_id == cart.id)
#         )
#         await db.commit()
#         return True


# class CartRepository(ICartRepository):
#     async def get_cart_by_user_id(self, user_id: int, db: AsyncSession) -> Cart | None:
#         query = select(Cart).where(Cart.user_id == user_id).options(
#             joinedload(Cart.cart_items).joinedload(CartItem.product)
#         )
#         result = await db.execute(query)
#         return result.scalar_one_or_none()
#
#     async def create_cart(self, user_id: int, db: AsyncSession) -> Cart:
#         new_cart = Cart(user_id=user_id)
#         db.add(new_cart)
#         await db.commit()
#         await db.refresh(new_cart)
#         return new_cart
#
#     async def add_item_to_cart(self, cart_id: int, product_id: int, quantity: int, sum_price: float, db: AsyncSession) -> CartItem:
#         new_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity, sum_price=sum_price)
#         db.add(new_item)
#         await db.commit()
#         await db.refresh(new_item)
#         return new_item
#
#     async def remove_item(self, cart_item_id: int, db: AsyncSession) -> CartItem | None:
#         query = select(CartItem).where(CartItem.id == cart_item_id)
#         result = await db.execute(query)
#         cart_item = result.scalar_one_or_none()
#         if cart_item:
#             await db.delete(cart_item)
#             await db.commit()
#         return cart_item
#
#     async def clear_cart(self, cart_id: int, db: AsyncSession) -> None:
#         query = select(CartItem).where(CartItem.cart_id == cart_id)
#         result = await db.execute(query)
#         items = result.scalars().all()
#         for item in items:
#             await db.delete(item)
#         await db.commit()