from datetime import datetime, timedelta, timezone
import bcrypt
from app.core.config import settings
from jose import JWTError, jwt

def get_password_hash(password: str) -> str:
    """Encrypt the password."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the plain password matches the hashed password."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.SECURITY_SECRET_KEY,
        algorithm=settings.SECURITY_ALGORITHM,
    )


def create_refresh_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.SECURITY_REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.SECURITY_SECRET_KEY,
        algorithm=settings.SECURITY_ALGORITHM,
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.SECURITY_SECRET_KEY,
            algorithms=[settings.SECURITY_ALGORITHM],
        )
    except JWTError:
        return {}
