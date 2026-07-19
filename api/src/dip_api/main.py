from fastapi import Depends, FastAPI

from dip_api.config import Settings, get_settings

app = FastAPI(title="DIP API", version="0.1.0")

app_settings = get_settings()


@app.get("/health")
async def health_check(
    settings: Settings = Depends(lambda: app_settings),
) -> dict[str, str]:
    """
    Health check endpoint to verify that the API is running.
    """
    return {
        "status": "ok",
        "api_host": settings.api_host,
        "api_port": str(settings.api_port),
        "log_level": settings.log_level,
    }
