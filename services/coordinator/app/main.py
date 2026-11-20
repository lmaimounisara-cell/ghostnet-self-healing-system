from fastapi import FastAPI

app = FastAPI(title="GhostNet Coordinator")


@app.get("/health")
def health():
    return {"status": "ok"}