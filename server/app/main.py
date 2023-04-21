from fastapi import FastAPI

from app.routers import games_router, recommendations_router

app = FastAPI()
app.include_router(games_router.router)
app.include_router(recommendations_router.router)


@app.get("/")
@app.get("/health")
def health_check() -> str:
    return "Server OK"
