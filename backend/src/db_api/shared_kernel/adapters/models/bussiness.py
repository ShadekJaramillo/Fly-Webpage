from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...domain.entities import ChineseLevel as Level
from .application import User
from .base import Base, TableNames
from .mixins import IdMixin

"""
This module contains the SQLAlchemy models related to the company bussiness 
model and structure.
"""


class Athlete(IdMixin, Base):
  __tablename__ = TableNames.ATHLETES
  active: Mapped[bool] = mapped_column(Boolean, default=True)
  user_id: Mapped[int] = mapped_column(ForeignKey(f"{TableNames.USERS}.id"))
  trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id"))
  chinese_level: Mapped[Level] = mapped_column(Enum(Level))
  date_joined: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
  )

  user: Mapped["User"] = relationship(back_populates="athlete")
  trainer: Mapped["Trainer"] = relationship(back_populates="athletes")


class Trainer(IdMixin, Base):
  __tablename__ = TableNames.TRAINERS
  active: Mapped[bool] = mapped_column(Boolean, default=True)
  user_id: Mapped[int] = mapped_column(ForeignKey(f"{TableNames.USERS}.id"))
  chinese_level: Mapped[Level] = mapped_column(Enum(Level))
  date_joined: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
  )

  user: Mapped["User"] = relationship(back_populates="trainer")
  athletes: Mapped["Athlete"] = relationship(back_populates="trainer")
