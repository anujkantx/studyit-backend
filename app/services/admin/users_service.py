from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.users import User


class UsersService:
	@staticmethod
	async def all_users(db: AsyncSession):
		result = await db.execute(
			select(User).options(selectinload(User.role)).order_by(User.id)
		)
		return list(result.scalars().all())
