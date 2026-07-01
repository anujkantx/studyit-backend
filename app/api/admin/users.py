from fastapi import APIRouter, Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.schemas.admin.users import UserResponse
from app.services.admin.users_service import UsersService

router = APIRouter(prefix="/admin", tags=["users"])

@router.get("/allusers", response_model=list[UserResponse])
async def list_users(request:Request, db: AsyncSession = Depends(get_db) ):
    # token = request.cookies.get("access_token")

    return await UsersService.all_users(db)