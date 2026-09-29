from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., description="Username of the user or their email address")
    password: str = Field(..., description="Password of the user")

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    must_change_password: bool