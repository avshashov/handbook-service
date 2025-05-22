from fastapi import APIRouter

from app.api.v1 import organization

router_v1 = APIRouter(prefix='/v1')
router_v1.include_router(organization.router)
