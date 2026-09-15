from fastapi import FastAPI

import app.models

from app.api.ingestion import router as ingestion_router


app = FastAPI(
    title="Email Security Platform",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(ingestion_router)