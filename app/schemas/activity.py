from pydantic import BaseModel, ConfigDict


class ActivityDTO(BaseModel):
    activity_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
