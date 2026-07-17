from contextlib import asynccontextmanager

from fastapi import FastAPI

from dip_api.config import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    app.state._state["settings"] = settings
    yield


app = FastAPI(title="DIP API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "ok"}
