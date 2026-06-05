from pydantic import BaseModel

class GoogleAuthRequest(BaseModel):
    token: str
    
class UserInfo(BaseModel):
    id: int
    name: str
    email: str
    avatar_url: str | None = None
    role: str


class GoogleAuthResponse(BaseModel):
    success: bool
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserInfo