from fastapi import APIRouter
from app.schemas.auth.google import GoogleAuthRequest
from app.services.auth.google import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/google")
async def google_auth(request: GoogleAuthRequest):
    print("Received Google auth request with token:")


    token_info = await AuthService.verify_google_token(request.token)

    print("Google token verification returned info:", token_info)

    print("sending response with token info")
    return {"success": True, "token_info": token_info}