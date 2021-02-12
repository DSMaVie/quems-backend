from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, String, create_engine
from Pathlib import Path
import os

base = declarative_base()


class Database:
    def __init__(self, path_to_db: Path):
        self.path = path_to_db

        db_url = "sqlite:///" + str(path_to_db.resolve())
        self.engine = create_engine(db_url, echo=os.getenv("DB_VERBOSITY", False))
        # TODO: actually create tables https://docs.sqlalchemy.org/en/13/orm/tutorial.html


class EventTable(base):
    __tablename__ = "events"

    ID = Column(Integer, primary_key=True)
    time = Column(Integer, nullable=False)
    recurring = Column(Boolean, nullable=False)
    dID = Column(Integer, nullable=False)


class RecurringEvents(base):
    __tablename__ = "recurring_events"

    ID = Column(Integer, primary_key=True)
    place = Column(String, nullable=False)
    regularity = Column(String, nullable=False)
    outdated = Column(Boolean, nullable=False)
    name_de = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    end = Column(Integer)
    desc_de = Column(String, nullable=False)
    desc_en = Column(String, nullable=False)
    assignees = Column(String, nullable=False)
    nl = Column(Boolean, nullable=False)
    insta = Column(Boolean, nullable=False)
    fb = Column(Boolean, nullable=False)
    twitter = Column(Boolean, nullable=False)
    discord = Column(Boolean, nullable=False)


class SingularEvents(base):
    __tablename__ = "singular_events"

    ID = Column(Integer, primary_key=True)
    place = Column(String, nullable=False)
    regularity = Column(String, nullable=False)
    outdated = Column(Boolean, nullable=False)
    name_de = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    end = Column(Integer)
    desc_de = Column(String, nullable=False)
    desc_en = Column(String, nullable=False)
    assignees = Column(String, nullable=False)
    nl = Column(Boolean, nullable=False)
    insta = Column(Boolean, nullable=False)
    fb = Column(Boolean, nullable=False)
    twitter = Column(Boolean, nullable=False)
    discord = Column(Boolean, nullable=False)
