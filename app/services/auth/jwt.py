from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.settings import settings

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM

class JWTService:

    @staticmethod
    def create_access_token(data: dict):
        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire, "type": "access", "iat": datetime.now(timezone.utc)})
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict):
        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        payload.update({"exp": expire, "type": "refresh", "iat": datetime.now(timezone.utc)})
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_jwt_token(token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise Exception("Token has expired")
        except JWTError:
            raise Exception("Invalid token")

    @staticmethod
    def verify_access_token(token: str):
        payload = JWTService.verify_jwt_token(token)
        if payload.get("type") != "access":
            raise Exception("Invalid token type")
        return payload

    @staticmethod
    def verify_refresh_token(token: str):
        payload = JWTService.verify_jwt_token(token)
        if payload.get("type") != "refresh":
            raise Exception("Invalid token type")
        return payload