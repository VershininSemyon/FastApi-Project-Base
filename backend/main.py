
from contextlib import asynccontextmanager

import uvicorn
from api.routers.auth import auth_router
from api.routers.healthcheck import healthcheck_router
from api.routers.user import user_router
from config.settings import settings
from db.database import engine
from exceptions.base import AppError
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(healthcheck_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=settings.UVICORN_RELOAD,
        workers=settings.UVICORN_WORKERS_COUNT
    )
