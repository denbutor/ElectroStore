from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from app.db.schemas.user import UserUpdate
from app.exceptions import NotFoundUserException


class UserRepository:
    @staticmethod
    async def get_all_users(db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    # async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    #     return await db.execute(select(User).where(User.id == user_id))

    @staticmethod
    async def create_user(db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return None
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise NotFoundUserException()
        await db.delete(user)
        await db.commit()
        return True


    # @staticmethod
    # async def update_user(db: AsyncSession, user_id: int, user_data: dict) -> User:
    #     user = await UserRepository.get_user_by_id(db, user_id)
    #     if not user:
    #         raise NotFoundUserException()
    #
    #     for key, value in user_data.items():
    #         if hasattr(user, key) and value is not None:
    #             setattr(user, key, value)
    #
    #     await db.commit()
    #     await db.refresh(user)
    #     return user


# class UserRepository(IUserRepository):
#         def __init__(self, db: AsyncSession):
#             self.db = db
#
#     async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
#         result = await db.execute(select(User).where(User.email == email))
#         return result.scalars().first()
#
#     async def get_user_by_id(self, db: AsyncSession, user_id: int):
#         result = await db.execute(select(User).where(User.id == user_id))
#         return result.scalars().first()
#
#     async def create_user(self, db: AsyncSession, user: User) -> User:
#         db.add(user)
#         await db.commit()
#         await db.refresh(user)
#         return user


# class UserRepository(IUserRepository):
#     def __init__(self, db: AsyncSession):
#         self.db = db
#
#     async def create_user(self, user: User) -> User:
#         self.db.add(user)
#         await self.db.commit()
#         await self.db.refresh(user)
#         return user
#
#     async def get_user_by_email(self, db: AsyncSession, email: str) -> User | None:
#         result = await db.execute(select(User).where(User.email == email))
#         return result.scalars().first()
#
#     async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User | None:
#         result = await db.execute(select(User).where(User.id == user_id))
#         return result.scalars().first()
#
#     async def create_user(self, db: AsyncSession, user: User) -> User:
#         db.add(user)
#         await db.commit()
#         await db.refresh(user)
#         return user
