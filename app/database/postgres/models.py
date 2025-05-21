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

    @classmethod
    async def get_by_activity_ids(cls, session: AsyncSession, activity_ids: list[int]) -> list[typing.Self]:
        if not activity_ids:
            return []

        query = (
            select(cls)
            .join(Activity.organizations)
            .where(Activity.activity_id.in_(activity_ids))
            .options(selectinload(cls.phones), selectinload(cls.activities), selectinload(cls.building))
        )

        result = await session.execute(query)
        return list(result.scalars().unique())

    @classmethod
    async def get_by_bounding_box(
        cls, session: AsyncSession, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> list[typing.Self]:
        query = (
            select(cls)
            .join(Building)
            .where(Building.latitude.between(min_lat, max_lat), Building.longitude.between(min_lon, max_lon))
            .options(selectinload(cls.phones), selectinload(cls.building), selectinload(cls.activities))
        )

        result = await session.execute(query)
        return list(result.scalars())

    @classmethod
    async def get_by_id(cls, session: AsyncSession, organization_id: int) -> typing.Self | None:
        query = (
            select(cls)
            .where(cls.organization_id == organization_id)
            .options(selectinload(cls.phones), selectinload(cls.building), selectinload(cls.activities))
        )
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def search_by_name(cls, session: AsyncSession, name: str) -> list[typing.Self]:
        result = await session.execute(
            select(cls)
            .join(Building)
            .where(cls.name.like(f'%{name}%'))
            .options(selectinload(cls.phones), selectinload(cls.building), selectinload(cls.activities))
        )
        return list(result.scalars())


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

    @classmethod
    async def get_all_child_activity_ids(cls, session: AsyncSession, root_activity_id: int) -> list[int]:
        cte = select(cls.activity_id).where(cls.activity_id == root_activity_id).cte(recursive=True)
        cte = cte.union_all(select(cls.activity_id).join(cte, cls.parent_id == cte.c.activity_id))

        result = await session.execute(select(cte.c.activity_id))
        return list(result.scalars())


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
