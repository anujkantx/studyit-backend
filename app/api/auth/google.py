from fastapi import APIRouter, Depends

from app.schemas.auth.google import GoogleAuthRequest, GoogleAuthResponse, UserInfo

from app.services.auth.google import GoogleAuthService
from app.services.auth.jwt import JWTService
from app.services.users.get_users import get_users
from app.services.users.create_users import create_users

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/google", response_model=GoogleAuthResponse)
async def google_auth(request: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):

    google_info = await GoogleAuthService.verify_google_token(request.token)
    user = await get_users.get_by_google_id(db, google_info["sub"])
    if not user:
        user = await create_users.create_by_google_info(db, google_info)

    payload = {"sub": str(user.id)}
    access_token = JWTService.create_access_token(payload)
    refresh_token = JWTService.create_refresh_token(payload)

    return GoogleAuthResponse(
        success=True,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserInfo(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar_url=user.avatar_url,
            role=user.role.name
        )
    )