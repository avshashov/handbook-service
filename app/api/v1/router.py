from fastapi import APIRouter

from app.api.v1 import organization

router = APIRouter(prefix='/v1')
router.include_router(organization.router)
