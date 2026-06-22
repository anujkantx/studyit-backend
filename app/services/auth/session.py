from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.models.users import RefreshSession
from typing import Optional

class SessionService:
    @staticmethod
    async def get_session_by_user_id(db: AsyncSession, user_id: int) -> Optional[RefreshSession]:
        result = await db.execute(
            select(RefreshSession).options(selectinload(RefreshSession.user)).where(RefreshSession.user_id == user_id)
        )
        return result.scalars().first()