from sqlalchemy.orm import as_declarative
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, select


@as_declarative()
class BaseTable:
    id = Column(Integer, primary_key=True)

    @classmethod
    def get_id(cls, session, **kwargs):
        stmt = select(cls.id).filter_by(**kwargs)
        result = session.execute(stmt)
        return result.scalar()

    @classmethod
    def drop_non_columns(cls, dict):
        cols = cls.__table__.columns.keys()
        return {key: dict[key] for key in dict if key in cols}

    def to_dict(self):
        cols = self.__table__.columns.keys()
        return {key: getattr(self, key) for key in cols}


class Event(BaseTable):
    __tablename__ = "events"
    # TODO: sqlalchemy has datetime datatype which is represented as string buttype checked for datetime python obj before insertion
    start = Column(Integer, nullable=False)
    end = Column(Integer)
    data_id = Column(Integer, ForeignKey("data.id"), nullable=False)
    created = Column(Integer, nullable=False)  # when using datetime set default to now
    last_edited = Column(Integer)


class Data(BaseTable):
    __tablename__ = "data"

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    reg_id = Column(Integer, ForeignKey("regularities.id"))
    assignee = Column(String, nullable=False)
    name_de = Column(String, nullable=False)
    name_en = Column(String)
    desc_de = Column(String)
    desc_en = Column(String)
    fb = Column(Boolean, nullable=False, default=False)
    insta = Column(Boolean, nullable=False, default=False)
    twitter = Column(Boolean, nullable=False, default=False)
    discord = Column(Boolean, nullable=False, default=False)
    nl = Column(Boolean, nullable=False, default=False)
    calendar = Column(Boolean, nullable=False, default=False)


class Place(BaseTable):
    __tablename__ = "places"

    name = Column(String, nullable=False)


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
