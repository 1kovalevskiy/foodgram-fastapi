import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.custom_middlewares import LoggingSystem
from core.exceptions import CustomException

from api.api_router import api_router
from core import settings


app = FastAPI(title=settings.PROJECT_NAME, docs_url="/documentation/")
app.add_middleware(LoggingSystem)
app.include_router(api_router, prefix='/api')


@app.exception_handler(CustomException)
async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content=exc.message,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
