from pydantic import BaseModel, ConfigDict

from app.schemas.activity import ActivityDTO
from app.schemas.building import BuildingDTO


class OrganizationDTO(BaseModel):
    name: str
    phone_number: str | None = None
    building: BuildingDTO
    activities: list[ActivityDTO]

    model_config = ConfigDict(from_attributes=True)


class OrganizationsSchema(BaseModel):
    organizations: list[OrganizationDTO]
