from fastapi import FastAPI
from app.routers import estimates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "https://tti.velocityexplorations.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    estimates.router,
    prefix="/api/estimates",
    tags=["estimates"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}