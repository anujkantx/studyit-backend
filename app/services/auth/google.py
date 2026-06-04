import base64
import json

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi import HTTPException, status

from app.core.config import settings

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID

class AuthService:

    @staticmethod
    async def verify_google_token(token: str):
        try:
            if not GOOGLE_CLIENT_ID:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="GOOGLE_CLIENT_ID is not configured"
                )

            print("google_auth: Verifying token with Google...")

            id_info = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                GOOGLE_CLIENT_ID,
                clock_skew_in_seconds=60
            )
            
            return id_info

            

        except Exception as e:
            print("Unexpected Google token verification error:", repr(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Google token verification failed: {e}"
            )

            