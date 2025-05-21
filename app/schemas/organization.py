from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.activity import ActivityDTO
from app.schemas.building import BuildingDTO
from app.schemas.phone import PhoneDTO


class OrganizationDTO(BaseModel):
    name: str
    phones: list[str]
    building: BuildingDTO
    activities: list[ActivityDTO]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('phones', mode='before')
    @classmethod
    def get_phone_numbers(cls, field: list[PhoneDTO]) -> list[str]:
        if not field:
            return []
        return [phone.number for phone in field]


class OrganizationsSchema(BaseModel):
    organizations: list[OrganizationDTO]
