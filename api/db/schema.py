from sqlalchemy.orm import as_declarative, relationship
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
    created = Column(Integer, nullable=False)  # when using datetime set default to now
    last_edited = Column(Integer)

    data_id = Column(Integer, ForeignKey("data.id"), nullable=False)
    data = relationship(
        "Data", uselist=False, foreign_keys=data_id
    )  # , primary_join=Data.id == Event.data_id )

    def unpack(self):
        result_dict = self.to_dict()
        del result_dict["data_id"]
        result_dict |= self.data.unpack()
        return result_dict


class Data(BaseTable):
    __tablename__ = "data"

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

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    place = relationship(
        "Place", uselist=False, foreign_keys=place_id
    )  # , primary_join=Place.id == Data.place_id)

    reg_id = Column(Integer, ForeignKey("regularities.id"))
    reg = relationship(
        "Regularity", uselist=False, foreign_keys=reg_id
    )  # , primary_join=Regularity.id == Data.reg_id)

    def unpack(self):
        result_dict = self.to_dict()

        del result_dict["place_id"]
        del result_dict["reg_id"]

        result_dict |= {"place": self.place.name}
        if self.reg_id is not None:
            result_dict |= self.reg.to_dict()

        return result_dict


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
