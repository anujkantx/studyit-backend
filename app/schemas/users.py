from pydantic import BaseModel

class RoleResponse(BaseModel):
    id: int
    name: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    avatar_url: str | None
    status: str
    role_id: int
    role: RoleResponse

class CreateUserRequest(BaseModel):
    name: str
    email: str
    phone: str | None