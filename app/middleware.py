from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, app_key: str):
        super().__init__(app)
        self.app_key = app_key
        self.public_paths = {'/docs', '/redoc', '/openapi.json'}

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.url.path in self.public_paths:
            return await call_next(request)

        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != self.app_key:
            return JSONResponse(status_code=403, content={'detail': 'Missing or invalid API key'})

        response = await call_next(request)
        return response
