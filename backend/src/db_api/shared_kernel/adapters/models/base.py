from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# from dotenv import load_dotenv
# import os
# url = os.getenv()
"""
Decalarative base for all the SQLAlchemy models of the API. 
"""
engine = create_engine("sqlite:///:memory:")
get_session = sessionmaker(engine)


class Base(DeclarativeBase):
  pass


# TODO Evaluate if instead of using the `TableName` pattern, it would be better
# to define the tables and models separatedly.
# NOTE since we are in early stages of the development it is useful to have a
# single place where all the table names are difined, this way if a table name
# changes there is no need to manually replace the text on every `ForeignKey`.
class TableNames(Enum):
  # application module
  USERS = "users"
  USER_INFOS = "user_infos"
  ACCESS_TYPES = "access_types"

  # bussiness module
  CHINESE_LEVELS = "chinese_levels"
  ATHLETES = "athletes"
  TRAINERS = "trainers"
