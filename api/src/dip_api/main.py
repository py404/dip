from fastapi import FastAPI

app = FastAPI(title="DIP API", version="0.1.0")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "ok"}
