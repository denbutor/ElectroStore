from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.cart import Cart
from app.db.models.cart_item import CartItem
from app.db.repositories.cart_repository import CartRepository
from app.db.repositories.icart_repository import ICartRepository
from app.db.schemas.cart import CartResponse, CartItemCreate, CartItemResponse

class CartService:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    # async def get_cart(self, user_id: int, db: AsyncSession) -> CartResponse | None:
    #     cart = await self.cart_repo.get_cart_by_user_id(user_id, db)
    #     if not cart:
    #         return None
    #
    #     cart_items = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id))
    #     items = cart_items.scalars().all()
    #
    #     return CartResponse(
    #         id=cart.id,
    #         user_id=cart.user_id,
    #         cart_items=[CartItemResponse.model_validate(item) for item in items]
    #     )

    async def get_cart(self, user_id: int, db: AsyncSession) -> CartResponse | None:
        cart = await self.cart_repo.get_cart_by_user_id(user_id, db)
        if not cart:
            return None
        return CartResponse.model_validate(cart)

    async def create_cart(self, user_id: int, db: AsyncSession) -> CartResponse:
        cart = await self.cart_repo.create_cart(user_id, db)
        return CartResponse(id=cart.id, user_id=cart.user_id, cart_items=[])

    async def add_to_cart(self, db: AsyncSession, user_id: int, product_id: int, quantity: int) -> CartItemResponse:
        cart_item = await self.cart_repo.add_to_cart(db, user_id, product_id, quantity)
        return CartItemResponse.model_validate(cart_item)

    async def remove_from_cart(self, user_id: int, product_id: int, db: AsyncSession) -> bool:
        return await self.cart_repo.remove_from_cart(db, user_id, product_id)

    async def clear_cart(self, user_id: int, db: AsyncSession) -> bool:
        return await self.cart_repo.clear_cart(db, user_id)

# class CartService:
#     def __init__(self, cart_repo: CartRepository):
#         self.cart_repo = cart_repo
#
#     # async def get_cart(self, user_id: int, db: AsyncSession) -> CartResponse | None:
#     #     cart = await self.cart_repo.get_cart_by_user_id(user_id, db)
#     #     if not cart:
#     #         return None
#     #     cart_items = await db.execute(
#     #         select(CartItem).where(CartItem.cart_id == cart.id)
#     #     )
#     #     items = cart_items.scalars().all()
#     #     return CartResponse(id=cart.id, user_id=cart.user_id, items=[item for item in items])
#
#     async def get_cart(self, user_id: int, db: AsyncSession) -> CartResponse | None:
#         cart = await self.cart_repo.get_cart_by_user_id(user_id, db)
#         if not cart:
#             return None
#         # Отримуємо елементи кошика
#         cart_items = await db.execute(
#             select(CartItem).where(CartItem.cart_id == cart.id)
#         )
#         items = cart_items.scalars().all()
#         # Створюємо відповідь
#         return CartResponse(id=cart.id, user_id=cart.user_id, items=[CartItemResponse.model_dump(item) for item in items])
#
#     async def create_cart(self, user_id: int, db: AsyncSession) -> CartResponse:
#         cart = await self.cart_repo.create_cart(user_id, db)
#         return CartResponse(id=cart.id, user_id=cart.user_id, items=[])
#
#     # async def add_to_cart(self, user_id: int, product_id: int, quantity: int, db: AsyncSession) -> CartItem:
#     #     return await self.cart_repo.add_to_cart(db, user_id, product_id, quantity)
#
#     async def add_to_cart(self, db: AsyncSession, user_id: int, product_id: int, quantity: int) -> CartItem:
#         # Знаходимо кошик користувача
#         cart = await self.cart_repo.get_cart_by_user_id(user_id, db)
#         if not cart:
#             # Якщо кошика немає, створюємо новий
#             cart = await self.create_cart(user_id, db)
#
#         # Перевірка, чи є вже товар в кошику
#         existing_item = await db.execute(
#             select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
#         )
#         existing_item = existing_item.scalar_one_or_none()
#
#         if existing_item:
#             # Якщо товар вже є, оновлюємо кількість
#             existing_item.quantity += quantity
#             await db.commit()
#             await db.refresh(existing_item)
#             return existing_item
#         else:
#             # Якщо товару немає в кошику, додаємо новий CartItem
#             new_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity,
#                                 sum_price=0)  # sum_price можна обчислювати окремо
#             db.add(new_item)
#             await db.commit()
#             await db.refresh(new_item)
#             return new_item
#
#     async def remove_from_cart(self, user_id: int, product_id: int, db: AsyncSession) -> bool:
#         return await self.cart_repo.remove_from_cart(db, user_id, product_id)
#
#     async def clear_cart(self, user_id: int, db: AsyncSession) -> bool:
#         return await self.cart_repo.clear_cart(db, user_id)



# class CartService:
#     def __init__(self, cart_repo: ICartRepository):
#         self.cart_repo = cart_repo
#
#     async def get_or_create_cart(self, user_id: int, db: AsyncSession) -> CartResponse:
#         cart = await self.cart_repo.get_cart_by_user_id(user_id, db)
#         if not cart:
#             cart = await self.cart_repo.create_cart(user_id, db)
#         return CartResponse.model_validate(cart)
#
#     async def add_item(self, user_id: int, item_data: CartItemCreate, db: AsyncSession) -> CartItemResponse:
#         cart = await self.get_or_create_cart(user_id, db)
#         cart_item = await self.cart_repo.add_item_to_cart(
#             cart.id, item_data.product_id, item_data.quantity, item_data.sum_price, db
#         )
#         return CartItemResponse.model_validate(cart_item)
#
#     async def remove_item(self, cart_item_id: int, db: AsyncSession) -> CartItemResponse | None:
#         cart_item = await self.cart_repo.remove_item(cart_item_id, db)
#         return CartItemResponse.model_dump(cart_item) if cart_item else None
#
#     async def clear_cart(self, user_id: int, db: AsyncSession) -> None:
#         cart = await self.cart_repo.get_cart_by_user_id(user_id, db)
#         if cart:
#             await self.cart_repo.clear_cart(cart.id, db)
