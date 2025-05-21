import typing

from sqlalchemy import NUMERIC, Column, ForeignKey, Integer, String, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload, validates

from app.database.postgres.base import Base

organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organization.organization_id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activity.activity_id'), primary_key=True),
)


class Organization(Base):
    __tablename__ = 'organization'

    organization_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    building_id: Mapped[int] = mapped_column(Integer, ForeignKey('building.building_id'), nullable=False)

    building: Mapped['Building'] = relationship('Building', back_populates='organizations')  # noqa: F821
    activities: Mapped[list['Activity']] = relationship(  # noqa: F821
        secondary=organization_activity, back_populates='organizations'
    )
    phones: Mapped[list['OrganizationPhone']] = relationship(  # noqa: F821
        'OrganizationPhone', back_populates='organization'
    )

    @classmethod
    async def get_by_building_id(cls, session: AsyncSession, building_id: int) -> list[typing.Self]:
        query = (
            select(cls)
            .where(cls.building_id == building_id)
            .options(
                selectinload(cls.building),
                selectinload(cls.phones),
                selectinload(cls.activities).selectinload(Activity.organizations),
            )
        )
        result = await session.execute(query)
        return list(result.scalars().unique())


class Activity(Base):
    __tablename__ = 'activity'

    activity_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    parent_id: Mapped[int] = mapped_column(
        ForeignKey('activity.activity_id', ondelete='CASCADE'), nullable=True
    )

    parent: Mapped[typing.Optional['Activity']] = relationship(
        'Activity', remote_side=[activity_id], back_populates='children'
    )
    children: Mapped[list['Activity']] = relationship('Activity', back_populates='parent')

    organizations: Mapped[list[Organization]] = relationship(
        secondary=organization_activity, back_populates='activities'
    )


class OrganizationPhone(Base):
    __tablename__ = 'organization_phone'

    phone_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey('organization.organization_id'))

    organization: Mapped[Organization] = relationship('Organization', back_populates='phones')


class Building(Base):
    __tablename__ = 'building'

    building_id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(NUMERIC(9, 6))
    longitude: Mapped[float] = mapped_column(NUMERIC(10, 6))

    organizations: Mapped[list[Organization]] = relationship('Organization', back_populates='building')

    @validates('latitude', 'longitude')
    def validate_geo_value(self, key: str, value: typing.Any) -> float:  # noqa: ANN401
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
