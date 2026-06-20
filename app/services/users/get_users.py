from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, HTTPException
from app.schemas.users import UserResponse, RoleResponse

from app.models.users import User

class get_users:
    @staticmethod
    async def get_by_user_id(db: AsyncSession, uid: int)-> UserResponse | None:
        user = await db.execute(select(User).options(selectinload(User.role)).where(User.id == uid))    
        user = user.scalar_one_or_none()
        print("Fetched user:", user.name)
        return user

    @staticmethod
    async def get_by_google_id(db: AsyncSession, google_id: str)-> UserResponse | None:
        user = await db.execute(select(User).options(selectinload(User.role)).where(User.google_id == google_id))
        # selectinload(User.role) is used to eagerly load the related Role object, so we can access user.role.name without an additional query. This is important for performance, especially if we need to access the user's role information frequently after fetching the user.
        return user.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str)-> UserResponse | None:
        user = await db.execute(select(User).options(selectinload(User.role)).where(User.email == email))
        # selectinload(User.role) is used to eagerly load the related Role object, so we can access user.role.name without an additional query. This is important for performance, especially if we need to access the user's role information frequently after fetching the user.
        return user.scalar_one_or_none()
