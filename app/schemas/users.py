from pydantic import BaseModel

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    status: str
    created_at: str
    updated_at: str | None
    last_login_at: str | None
    role: RoleResponse

class CreateUserRequest(BaseModel):
    name: str
    email: str
    phone: str | None