import hashlib
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.db.session import get_db
from app.models.users import RefreshSession
from app.schemas.auth.google import GoogleAuthRequest
from app.services.auth.google import GoogleAuthService
from app.services.auth.jwt import JWTService
from app.services.auth.session import SessionService
from app.services.users.get_users import get_users
from app.services.users.create_users import create_users


router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/google")
async def google_auth(request: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):

    # Verify the Google token and get user info
    google_info = await GoogleAuthService.verify_google_token(request.token)

    # Get/create user in the database
    user = await get_users.get_by_google_id(db, google_info["sub"])
    if not user:
        user = await create_users.create_by_google_info(db, google_info)

    # One active session per user: If a session already exists for this user, delete it before creating a new one.
    old_session = await SessionService.get_session_by_user_id(db, user.id)
    if old_session:
        await db.delete(old_session)
        await db.flush()

    user.last_login_at = datetime.utcnow()

    #Generate JWT tokens
    access_token = JWTService.create_access_token(user.id)
    refresh_token = JWTService.create_refresh_token(user.id)

    # Store the refresh token hash in the database
    refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    session = RefreshSession(
        user_id=user.id,
        refresh_token_hash=refresh_token_hash,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        is_revoked=False
    )
    db.add(session)
    await db.commit()

    response = JSONResponse(
        content={
            "success": True,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.name
            }
        }
    )

    # Access token Cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age= 60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Refresh token Cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS
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
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )
    user = await get_users.get_by_user_id(db, int(payload["sub"]))
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user

@router.post("/refresh")
async def refresh(request:Request, db:AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    payload = JWTService.verify_jwt_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )

    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

    user_id = int(payload["sub"])

    session = await SessionService.get_session_by_user_id(db, user_id)
    if not session:
        raise HTTPException(
            status_code=401,
            detail="Session not found"
        )

    if session.is_revoked or session.refresh_token_hash != token_hash or session.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    new_access_token = JWTService.create_access_token(session.user_id)

    response = JSONResponse(
        content={
            "success": True,
            "user": {
                "id": session.user_id,
            },
        }
    )

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        # domain="localhost",  # Set to your domain in production
        samesite="lax",
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES # 30 minutes for access token
    )
    return response

@router.post("/logout")
async def logout(request:Request, db:AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    payload = JWTService.verify_jwt_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )

    user_id = int(payload["sub"])
    session = await SessionService.get_session_by_user_id(db, user_id)
    if session:
        await db.delete(session)
        await db.commit()

    response = JSONResponse(
        content={
            "success": True,
            "message": "Logged out successfully"
        }
    )

    # Clear cookies
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return response