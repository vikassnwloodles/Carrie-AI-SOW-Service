import time
import logging
import traceback
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger("myapp.access")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as e:
            duration = time.time() - start_time
            client_ip = request.client.host
            method = request.method
            path = request.url.path
            user_agent = request.headers.get("user-agent", "-")

            logger.error(
                f'{client_ip} - "{method} {path}" 500 in {duration:.2f}s - UA: {user_agent} - Exception: {e}'
            )
            logger.debug("".join(traceback.format_exception(type(e), e, e.__traceback__)))

            # Return 500 error response
            return JSONResponse(
                {"detail": "Internal Server Error"},
                status_code=500
            )

        duration = time.time() - start_time
        client_ip = request.client.host
        method = request.method
        path = request.url.path
        status = response.status_code
        user_agent = request.headers.get("user-agent", "-")

        logger.info(
            f'{client_ip} - "{method} {path}" {status} in {duration:.2f}s - UA: {user_agent}'
        )

        return response
