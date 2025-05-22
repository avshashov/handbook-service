from fastapi import APIRouter

from app.api.v1.router import router_v1

main_router = APIRouter(prefix='/api')
main_router.include_router(router_v1)
