from fastapi import FastAPI
from sqlalchemy import text

from app.api.router import api_router
from app.db.session import engine

app = FastAPI(
    title="Help Desk Simulator API",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "application": "Help Desk Simulator",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.get("/health/database")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "status": "healthy",
    }
