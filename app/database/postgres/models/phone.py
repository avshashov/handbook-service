from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.postgres.models.base import Base


class OrganizationPhone(Base):
    __tablename__ = 'organization_phone'

    phone_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey('organization.organization_id'))

    organization: Mapped['Organization'] = relationship('Organization', back_populates='phones')  # noqa: F821
