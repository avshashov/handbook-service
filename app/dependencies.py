from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres.connection import database
from app.services.organization import OrganizationService

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]


def get_organization_service(session: SessionDep) -> OrganizationService:
    return OrganizationService(db_session=session)


OrgServiceDep = Annotated[OrganizationService, Depends(get_organization_service)]
