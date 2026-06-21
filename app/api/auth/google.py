from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse # for set cookie in response

from app.schemas.auth.google import GoogleAuthRequest

from app.services.auth.google import GoogleAuthService
from app.services.auth.jwt import JWTService
from app.services.users.get_users import get_users
from app.services.users.create_users import create_users

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/google")
async def google_auth(request: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):

    google_info = await GoogleAuthService.verify_google_token(request.token)
    user = await get_users.get_by_google_id(db, google_info["sub"])
    if not user:
        user = await create_users.create_by_google_info(db, google_info)

    payload = {"sub": str(user.id)}
    access_token = JWTService.create_access_token(payload)
    refresh_token = JWTService.create_refresh_token(payload)

    response = JSONResponse(
        content={
            "success": True,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.name
            },
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        domain="localhost",  # Set to your domain in production
        samesite="lax",
        max_age=30 * 60 # 30 minutes for access token
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        domain="localhost",  # Set to your domain in production
        samesite="lax",
        max_age=60 * 60 * 24 * 7  # 7 days for refresh token
    )
    return response

from fastapi import Request, HTTPException
from app.schemas.users import UserResponse, RoleResponse

@router.get("/me", response_model=UserResponse)
async def get_me(request:Request, db:AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    payload = JWTService.verify_jwt_token(token)
    user = await get_users.get_by_user_id(db, int(payload["sub"]))
    return user

