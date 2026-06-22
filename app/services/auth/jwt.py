from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.settings import settings

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM

class JWTService:

    @staticmethod
    def create_access_token(user_id: int):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            }

        return jwt.encode(
            payload,
            JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM
            )

    @staticmethod
    def create_refresh_token(user_id: int):

        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            }
        return jwt.encode(
            payload, 
            JWT_SECRET_KEY, 
            algorithm=JWT_ALGORITHM
            )

    @staticmethod
    def verify_jwt_token(token: str):
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM]
                )
            return payload
        except ExpiredSignatureError:
            raise Exception(
                status_code=401, 
                detail="Token has expired"
                )
        except JWTError:
            raise Exception(
                status_code=401,
                detail="Invalid token"
                )
