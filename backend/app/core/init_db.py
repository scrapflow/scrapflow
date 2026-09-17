from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings

async def init_admin_user(db: AsyncSession):
    admin_user = settings.ADMIN_USER
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD
    
    # Execute in SQLAlchemy v2
    result = await db.execute(select(User).filter(User.username == admin_user))
    admin = result.scalars().first()
    
    if not admin:
        print(f"Admin ({admin_user}) does not exist. Creating now from .env...")
        new_admin = User(
            username=admin_user,
            email=admin_email,
            hashed_password=get_password_hash(admin_password), 
            is_active=True
        )
        db.add(new_admin)
        await db.commit()  # Save changes to the database
        print("Admin created successfully!")
    else:
        print("Admin already exists in the database.")
