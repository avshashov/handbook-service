from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.postgres.models.base import Base

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

    activities: Mapped[list['Activity']] = relationship(  # noqa: F821
        secondary=organization_activity, back_populates='organizations'
    )
