import time

import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from core.custom_middlewares import LoggingSystem
from db.base import get_session

from api.api_router import api_router
from core import settings


app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(LoggingSystem)
app.include_router(api_router, prefix='/api')


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
