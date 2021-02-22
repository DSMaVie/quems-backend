from abc import ABC
from sqlalchemy.orm import as_declarative
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, select


@as_declarative()
class BaseTable(ABC):
    id = Column(Integer, primary_key=True)

    @classmethod
    def get_id(cls, session, **kwargs):
        stmt = select(cls.id).where(cls(**kwargs))
        result = session.execute(stmt)
        return result.scalar()


class Event(BaseTable):
    __tablename__ = "events"
    # TODO: sqlalchemy has datetime datatype which is represented as string buttype checked for datetime python obj before insertion
    start = Column(Integer, nullable=False)
    end = Column(Integer)
    data_id = Column(Integer, ForeignKey("data.id"), nullable=False)
    created = Column(Integer, nullable=False)
    last_edited = Column(Integer)

    @classmethod
    def get_event(cls, id, **kwargs):
        raise NotImplementedError


class Data(BaseTable):
    __tablename__ = "data"

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    reg_id = Column(Integer, ForeignKey("regularities.id"))
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


class Place(BaseTable):
    __tablename__ = "places"

    name = Column(String, nullable=False)

    @classmethod
    def get_place(cls, session, place_id: str):
        raise NotImplementedError


class Regularity(BaseTable):
    __tablename__ = "regularities"

    outdated = Column(Boolean, nullable=False)
    ref_event = Column(Integer, ForeignKey("data.id"))
    ref_offset = Column(Integer)
    reg_base = Column(
        Integer
    )  # 0 -> every week, #1 -> every first [weekday], #2 -> every second [weekday], # -1 -> every last [weekday]
    reg_weekday = Column(Integer)

    # TODO: constraints for regularity params
