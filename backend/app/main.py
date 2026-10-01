import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.user import User  
from app.core.init_db import init_admin_user
from app.core.config import settings
from app.core.deps import get_current_user

from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.refresh import router as refresh_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initialize connection and table creation...")
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully.")
        
        async with AsyncSessionLocal() as db:
            await init_admin_user(db)
    except OSError as e:  
        print("ERROR: Cannot access the PostgreSQL database.")
        print("Check if the DB is running (port 5432).")
        print(f"Exact error: {e}")
        os._exit(1)
        
    yield
    
    print("Closing the DB connections...")
    await engine.dispose()
    print("The app is safely closed.")

app = FastAPI(lifespan=lifespan)

# Cors settings
if settings.ENVIRONMENT == "production":
    origins = [
        "https://example.com",
    ]
else:
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],   
)
# End Cors settings

app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
app.include_router(refresh_router, prefix="/api/v1", tags=["Authentication Refresh"])

@app.get("/")
def read_root(current_user: User = Depends(get_current_user)):
    return {"Message": "Testing it works!"}
