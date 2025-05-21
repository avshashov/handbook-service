from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgres.models.base import Base


class Activity(Base):
    __tablename__ = 'activity'

    activity_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    parent_id: Mapped[int] = mapped_column(
        ForeignKey('activity.activity_id', ondelete='CASCADE'), nullable=True
    )
