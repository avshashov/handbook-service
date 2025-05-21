import logging

from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.service import handbook_service

logger = logging.getLogger('uvicorn.error')
app: FastAPI = handbook_service.app


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.error(f'{request.method} {request.scope["path"]} {exc}')
    return await request_validation_exception_handler(request, exc)
