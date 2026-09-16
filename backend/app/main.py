import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import engine, Base
from app.models.user import User  

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initialize connection and table creation...")
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
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

@app.get("/")
def read_root():
    return {"Message": "Testing it works!"}
