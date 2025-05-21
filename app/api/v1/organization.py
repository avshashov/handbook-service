from fastapi import APIRouter, HTTPException

from app.dependencies import OrgServiceDep
from app.schemas.organization import OrganizationDTO, OrganizationsSchema

router = APIRouter(prefix='/organizations', tags=['Organizations'])


@router.get('/by-building/{building_id}')
async def get_organizations_by_building(building_id: int, service: OrgServiceDep) -> OrganizationsSchema:
    """
    ## Get organizations located in the specified building.

    ### Query parameters:
    - **building_id**: Identifier of the building to search for.

    ### Response:
    - List of organizations located in the given building.
    """
    return await service.get_organizations_by_building(building_id)


@router.get('/by-activity/{activity_id}')
async def get_organizations_by_activity(activity_id: int, service: OrgServiceDep) -> OrganizationsSchema:
    """
    ## Get organizations related to the specified activity.

    ### Query parameters:
    - **activity_id**: Identifier of the activity to filter organizations.

    ### Response:
    - List of organizations associated with the given activity.
    """
    return await service.get_organizations_by_activity(activity_id)


@router.get('/by-location')
async def get_organizations_in_area(
    min_lat: float, max_lat: float, min_lon: float, max_lon: float, service: OrgServiceDep
) -> OrganizationsSchema:
    """
    ## Get organizations located within the specified geographical area.

    ### Query parameters:
    - **min_lat**: Minimum latitude of the bounding box.
    - **max_lat**: Maximum latitude of the bounding box.
    - **min_lon**: Minimum longitude of the bounding box.
    - **max_lon**: Maximum longitude of the bounding box.

    ### Response:
    - List of organizations located within the defined rectangular area.
    """
    return await service.get_organizations_by_bounding_box(min_lat, max_lat, min_lon, max_lon)


@router.get('/by-id/{organization_id}')
async def get_organization_by_id(organization_id: int, service: OrgServiceDep) -> OrganizationDTO:
    """
    ## Get full information about a specific organization by ID.

    ### Path parameters:
    - **organization_id**: Unique identifier of the organization.

    ### Response:
    - Full details of the requested organization.
    - Returns 404 if the organization is not found.
    """
    organization = await service.get_organization_by_id(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail=f'Organization with id {organization_id} not found.')

    return organization


@router.get('/search')
async def search_organizations(name: str, service: OrgServiceDep) -> OrganizationsSchema:
    """
    ## Search organizations by name with partial match.

    ### Query parameters:
    - **name**: Search string used for matching against organization names.

    ### Response:
    - List of organizations whose names contain the provided query (case-sensitive).
    """
    return await service.get_by_name(name)


@router.get('/by-activity-with-children/{activity_id}')
async def get_organizations_by_activity_with_children(
    activity_id: int, service: OrgServiceDep
) -> OrganizationsSchema:
    """
    ## Get all organizations that belong to an activity and its child activities.

    ### Path parameters:
    - **activity_id**: Identifier of the root activity.

    ### Response:
    - List of organizations associated with the specified activity and any sub-activities under it.
    - Returns 404 if no organizations are found.
    """
    return await service.get_organizations_by_activity_with_children(activity_id)
