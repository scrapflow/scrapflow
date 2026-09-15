from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import engine, Base
from app.models.user import User  

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initialize connection and table creation...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    print("Closing the DB connections...")
    await engine.dispose()
    print("The app is safely closed.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Message": "Testing it works!"}
