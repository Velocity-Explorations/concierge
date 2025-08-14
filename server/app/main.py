from fastapi import FastAPI
from app.routers import estimates

app = FastAPI()

app.include_router(
    estimates.router,
    prefix="/api",
    tags=["estimates"]
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}