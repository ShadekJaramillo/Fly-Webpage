from typing import TYPE_CHECKING

from sqlalchemy import (
  Boolean,
  CheckConstraint,
  Enum,
  ForeignKey,
  String,
  or_,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...domain.entities import UserAccess
from .base import Base, TableNames
from .mixins import IdMixin

if TYPE_CHECKING:
  from .bussiness import Athlete, Trainer


"""
This module contains the SQLAlchemy models related to the application inner 
workings.
"""


class User(IdMixin, Base):
  __tablename__ = TableNames.USERS
  active: Mapped[bool] = mapped_column(Boolean, default=True)
  athlete_id: Mapped[int] = mapped_column(
    ForeignKey(f"{TableNames.ATHLETES}.id"), nullable=True
  )
  trainer_id: Mapped[int] = mapped_column(
    ForeignKey(f"{TableNames.TRAINERS}.id"), nullable=True
  )
  access_type: Mapped[UserAccess] = mapped_column(Enum(UserAccess))
  # NOTE Athlete and Trainer classes are not imported at runtime, so their
  # relationships need to include an argument referencing them.
  athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="user")
  trainer: Mapped["Trainer"] = relationship("Trainer", back_populates="user")
  user_info: Mapped["UserInfo"] = relationship(back_populates="user")

  __table_args__ = (
    CheckConstraint(
      or_(athlete_id.isnot(None), trainer_id.isnot(None)),
      name="athlete_or_trainer",
    ),
  )


class UserInfo(Base):
  __tablename__ = TableNames.USER_INFOS
  user_id: Mapped[int] = mapped_column(
    ForeignKey(f"{TableNames.USERS}"), primary_key=True
  )
  first_name: Mapped[str] = mapped_column(String(255))
  second_name: Mapped[str] = mapped_column(String(255))

  user: Mapped["User"] = relationship(back_populates="user_info")
