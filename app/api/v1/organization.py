from fastapi import APIRouter, HTTPException

from app.dependencies import SessionDep
from app.schemas.organization import OrganizationDTO, OrganizationsSchema
from app.services.organization import OrganizationService

router = APIRouter(prefix='/organizations', tags=['Organizations'])


@router.get('/by-building/{building_id}')
async def get_organizations_by_building(session: SessionDep, building_id: int) -> OrganizationsSchema:
    service = OrganizationService(session)
    return await service.get_organizations_by_building(building_id)


@router.get('/by-activity/{activity_id}')
async def get_organizations_by_activity(session: SessionDep, activity_id: int) -> OrganizationsSchema:
    service = OrganizationService(session)
    return await service.get_organizations_by_activity(activity_id)


@router.get('/by-location')
async def get_organizations_in_area(
    session: SessionDep, min_lat: float, max_lat: float, min_lon: float, max_lon: float
) -> OrganizationsSchema:
    service = OrganizationService(session)
    return await service.get_organizations_by_bounding_box(min_lat, max_lat, min_lon, max_lon)


@router.get('/by-id/{organization_id}')
async def get_organization_by_id(session: SessionDep, organization_id: int) -> OrganizationDTO:
    service = OrganizationService(session)
    organization = await service.get_organization_by_id(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail=f'Organization with id {organization_id} not found.')

    return await service.get_organization_by_id(organization_id)


@router.get('/search')
async def search_organizations(session: SessionDep, name: str) -> OrganizationsSchema:
    service = OrganizationService(session)
    return await service.get_by_name(name)


@router.get('/by-activity-with-children/{activity_id}')
async def get_organizations_by_activity_with_children(
    session: SessionDep, activity_id: int
) -> OrganizationsSchema:
    service = OrganizationService(session)
    return await service.get_organizations_by_activity_with_children(activity_id)
