from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import games_router, recommendations_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games_router.router)
app.include_router(recommendations_router.router)


@app.get("/")
@app.get("/health")
def health_check() -> str:
    return "Server OK"
