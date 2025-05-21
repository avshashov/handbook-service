from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres.models import Activity, Organization
from app.schemas.organization import OrganizationDTO, OrganizationsSchema


class OrganizationService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.org_db = Organization
        self.activity_db = Activity

    async def get_organizations_by_building(self, building_id: int) -> OrganizationsSchema:
        organizations = await self.org_db.get_by_building_id(
            session=self.db_session, building_id=building_id
        )
        organization_dtos = [OrganizationDTO.model_validate(org) for org in organizations]
        return OrganizationsSchema(organizations=organization_dtos)

    async def get_organizations_by_activity(self, activity_id: int) -> OrganizationsSchema:
        organizations = await self.org_db.get_by_activity_ids(
            session=self.db_session, activity_ids=[activity_id]
        )
        organization_dtos = [OrganizationDTO.model_validate(org) for org in organizations]
        return OrganizationsSchema(organizations=organization_dtos)

    async def get_organizations_by_bounding_box(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> OrganizationsSchema:
        organizations = await self.org_db.get_by_bounding_box(
            session=self.db_session, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon
        )
        organization_dtos = [OrganizationDTO.model_validate(org) for org in organizations]
        return OrganizationsSchema(organizations=organization_dtos)

    async def get_organization_by_id(self, org_id: int) -> OrganizationDTO | None:
        organization = await self.org_db.get_by_id(session=self.db_session, organization_id=org_id)
        if not organization:
            return None
        return OrganizationDTO.model_validate(organization)

    async def get_by_name(self, name: str) -> OrganizationsSchema:
        organizations = await self.org_db.search_by_name(session=self.db_session, name=name)
        organization_dtos = [OrganizationDTO.model_validate(org) for org in organizations]
        return OrganizationsSchema(organizations=organization_dtos)

    async def get_organizations_by_activity_with_children(self, activity_id: int) -> OrganizationsSchema:
        child_activity_ids = await self.activity_db.get_all_child_activity_ids(
            session=self.db_session, root_activity_id=activity_id
        )

        if not child_activity_ids:
            return OrganizationsSchema(organizations=[])

        organizations = await self.org_db.get_by_activity_ids(
            session=self.db_session, activity_ids=child_activity_ids
        )
        return OrganizationsSchema(
            organizations=[OrganizationDTO.model_validate(org) for org in organizations]
        )
