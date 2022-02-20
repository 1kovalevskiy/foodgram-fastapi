import time
import logging

from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from core.exceptions import CustomException

logging.basicConfig(
    level=logging.DEBUG,
    filename='foodgram_fastapi.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LoggingSystem(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            start_time = time.monotonic()
            response = await call_next(request)
            process_time = time.monotonic() - start_time
            logger.info(process_time)
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except CustomException as e:
            logger.error(e)
            raise e
        except Exception as e:
            logger.error(e)
            raise e
