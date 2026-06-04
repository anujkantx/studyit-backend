from pydantic import BaseModel, EmailStr
from datetime import datetime

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    status: str
    role: RoleResponse
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

