from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Imports from the database and models
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Schema Pydantic that defines the expected structure of the login request body
class LoginRequest(BaseModel):
    username: str = Field(..., description="Username of the user or their email address")
    password: str = Field(..., description="Password of the user")

# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/login")
async def login(
    login_data: LoginRequest,  # FastAPI will automatically validate the request body against this schema
    db: AsyncSession = Depends(get_db)
):
    """
    Login endpoint for user authentication. It checks the provided username/email and password against the database.
    If the credentials are valid, it returns a success message. Otherwise, it raises an HTTPException with an appropriate error message.
    """
    print(f"LOGIN Attempt for user: {login_data.username}")
    
    result = await db.execute(
        select(User).filter(
            (User.username == login_data.username) | (User.email == login_data.username)
        )
    )
    user = result.scalars().first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive account."
        )
        
    return {
        "message": "Login successful!", 
        "username": user.username,
        "email": user.email
    }
