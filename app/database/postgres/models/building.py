from typing import Any

from sqlalchemy import NUMERIC, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.database.postgres.models.base import Base


class Building(Base):
    __tablename__ = 'building'

    building_id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(NUMERIC(9, 6))
    longitude: Mapped[float] = mapped_column(NUMERIC(10, 6))

    @validates('latitude', 'longitude')
    def validate_geo_value(self, key: str, value: Any) -> float:  # noqa: ANN401
        if value is None:
            raise ValueError(f'{key} cannot be null')

        try:
            value_float = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'Invalid {key}: must be a number (got {value})') from exc

        if key == 'latitude' and not (-90 <= value_float <= 90):
            raise ValueError(f'Latitude must be between -90 and 90 (got {value_float})')

        if key == 'longitude' and not (-180 <= value_float <= 180):
            raise ValueError(f'Longitude must be between -180 and 180 (got {value_float})')

        return value_float
