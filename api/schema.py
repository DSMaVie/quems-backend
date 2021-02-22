from typing import Union, Dict
from sqlalchemy.orm import declacrative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

Base = declacrative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    start = Column(Integer, nullable=False)
    end = Column(Integer)
    data_id = Column(Integer, ForeignKey("data.id"), nullable=False)
    created = Column(Integer, nullable=False)
    last_edited = Column(Integer)

    @classmethod
    def get_event(cls, session, event: Dict[str, int]):
        raise NotImplementedError


class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    reg_id = (Column(Integer, ForeignKey("regularities.id")),)
    assignee = Column(String, nullable=False)
    name_de = Column(String, nullable=False)
    name_en = Column(String)
    desc_de = Column(String)
    desc_en = Column(String)
    fb = Column(Boolean, nullable=False)
    insta = Column(Boolean, nullable=False)
    twitter = Column(Boolean, nullable=False)
    discord = Column(Boolean, nullable=False)
    nl = Column(Boolean, nullable=False)
    calendar = Column(Boolean, nullable=False)

    @classmethod
    def get_id(cls, session, data: Dict[str, Union[str, int, bool]]):
        raise NotImplementedError


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    @classmethod
    def get_id(cls, session, place_name):
        raise NotImplementedError

    @classmethod
    def get_place(cls, session, place_id):
        raise NotImplementedError


class Regularity(Base):
    __tablename__ = "regularities"

    id = Column(Integer, primary_key=True)
    outdated = Column(Boolean, nullable=False)
    ref_event = Column(Integer, ForeignKey("data.id"))
    ref_offset = Column(Integer)
    reg_base = Column(
        Integer
    )  # 0 -> every week, #1 -> every first [weekday], #2 -> every second [weekday], # -1 -> every last [weekday]
    reg_weekday = Column(Integer)

    # TODO: contraints for regularity params

    @classmethod
    def get_last_id(cls, session):
        # for now this is enough. needs more complex getter logic later
        raise NotImplementedError
