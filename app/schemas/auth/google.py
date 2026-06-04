from pydantic import BaseModel

class GoogleAuthRequest(BaseModel):
    token: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    
class GoogleAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

