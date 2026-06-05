from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db

from app.schemas.admin.users import UserResponse
from app.services.admin.users_service import UsersService

router = APIRouter(prefix="/admin", tags=["users"])

@router.get("/allusers", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await UsersService.all_users(db)