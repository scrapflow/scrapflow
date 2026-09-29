from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import JSONResponse

# Imports from the database and models
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
    
# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post(
    "/login",
    responses={200: {"model": LoginResponse}},
)
async def login(
    login_data: LoginRequest,
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
        
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "must_change_password": user.must_change_password,
        }
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,          
        secure=True if settings.ENVIRONMENT == "production" else False, 
        max_age=7 * 24 * 60 * 60, 
        path="/api/v1/auth",           
    )

    return response
