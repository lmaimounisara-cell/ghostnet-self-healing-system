from fastapi import FastAPI

app = FastAPI(title="GhostNet Workers")


@app.get("/health")
def health():
    return {"status": "ok"}