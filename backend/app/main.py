from fastapi import FastAPI

app = FastAPI(
    title="Help Desk Simulator API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "application": "Help Desk Simulator",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }