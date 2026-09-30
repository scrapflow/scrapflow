from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.schemas.auth import LoginResponse
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication Refresh"])

@router.post("/refresh", response_model=LoginResponse)

async def refresh_session(
    response: Response,
    refresh_token: str | None = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token lipsă."
        )
    
    try:
        payload = decode_token(refresh_token) 
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalid sau expirat."
        )
        
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilizator invalid sau inactiv."
        )
        
    new_access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True if settings.ENVIRONMENT == "production" else False,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/api/v1/auth",
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "must_change_password": user.must_change_password,
    }