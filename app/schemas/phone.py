from pydantic import BaseModel, ConfigDict


class PhoneDTO(BaseModel):
    number: str

    model_config = ConfigDict(from_attributes=True)
