
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="GhostNet Coordinator")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)
