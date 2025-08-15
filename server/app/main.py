from fastapi import FastAPI
from app.routers import estimates

app = FastAPI()

app.include_router(
    estimates.router,
    prefix="/api/estimates",
    tags=["estimates"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}