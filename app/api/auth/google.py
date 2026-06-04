from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import GoogleAuthRequest, GoogleAuthResponse


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/google")
async def google_auth(request: GoogleAuthRequest) -> GoogleAuthResponse:
    try:
        # Call the service layer to handle Google authentication
        auth_response = await AuthService.google_login(request.token)
        print("Google Auth Response:", auth_response)
        return auth_response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))