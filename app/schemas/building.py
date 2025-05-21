from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class BuildingDTO(BaseModel):
    building_id: int
    address: str
    coordinates: tuple[float, float]

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='before')
    @classmethod
    def set_coordinates(cls, data: Any) -> Any:  # noqa: ANN401
        if hasattr(data, 'latitude') and hasattr(data, 'longitude'):
            data.coordinates = (data.latitude, data.longitude)
        return data
