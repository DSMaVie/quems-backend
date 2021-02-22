from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from schema import Event, Data, Place, Regularity, BaseTable

# from datetime import datetime as dt
# from dateutil.relativedelta import relativedelta
# from dateutil.utils import today
import os


class QueryManager:
    def __init__(self, path_to_db: Path):
        # load and wrap initialization vars
        debug = bool(os.getenv("DB_DEBUG", False))
        # need_dummy_data = bool(os.getenv("DB_FILL_WITH_DUMMIES", False))

        # define engine and meta
        db_url = "sqlite:///" + str(path_to_db.resolve())
        self.engine = create_engine(db_url, echo=debug)
        self.meta = BaseTable.metadata
        self.session = sessionmaker(self.engine, future=True)

        self.meta.create_all(bind=self.engine)

    def add_singular_event(self, *args, **kwargs):
        with self.session.begin() as sess:
            if (place_id := Place.get_id(sess, kwargs["place"])) is None:
                sess.add(Place(name=place_id))
                place_id = Place.get_id(sess, kwargs["place"])

            sess.add(Data(**kwargs, place_id=place_id))  # might need kwarg filtering
            data_id = Data.get_id(sess, **kwargs)

            sess.add(Event(**kwargs, data_id=data_id))
            event_id = Event.get_id(sess, **kwargs)
            return event_id


# DEPRECATED CODE BELOW
# class EventDatabase:
#     def __init__(self, path_to_db: Path):
#         self.path = path_to_db

#         # load and wrap initialization vars
#         debug = bool(os.getenv("DB_DEBUG", False))
#         need_dummy_data = bool(os.getenv("DB_FILL_WITH_DUMMIES", False))
#         db_url = "sqlite:///" + str(path_to_db.resolve())

#         # define engine and meta
#         self.engine = create_engine(db_url, echo=debug)
#         self.meta = MetaData()

#         # define tables
#         self.events = Table(
#             "events",
#             self.meta,
#             Column(
#                 "id", Integer, primary_key=True
#             ),  # if not explicitly set is autoincremented
#             Column("start", Integer, nullable=False),
#             Column("end", Integer),
#             Column("data_id", Integer, ForeignKey("data.data_id"), nullable=False),
#             Column("created", Integer, nullable=False),
#             Column("last_edited", Integer),
#         )
#         self.data = Table(
#             "data",
#             self.meta,
#             Column("data_id", Integer, primary_key=True),
#             Column("place_id", Integer, ForeignKey("place.place_id"), nullable=False),
#             Column("reg_id", Integer, ForeignKey("regularity.reg_id")),
#             Column("name_de", String, nullable=False),
#             Column("name_en", String, nullable=False),
#             Column("assignee", String, nullable=False),
#             Column("desc_de", String),
#             Column("desc_en", String),
#             Column("fb", Boolean, nullable=False),
#             Column("insta", Boolean, nullable=False),
#             Column("twitter", Boolean, nullable=False),
#             Column("discord", Boolean, nullable=False),
#             Column("nl", Boolean, nullable=False),
#             Column("calendar", Boolean, nullable=False),
#         )
#         self.places = Table(
#             "place",
#             self.meta,
#             Column("place_id", Integer, primary_key=True),
#             Column("name", String, nullable=False, unique=True),
#         )
#         self.regularities = Table(
#             "regularity",
#             self.meta,
#             Column("reg_id", Integer, primary_key=True),
#             Column("outdated", Boolean, nullable=False),  # needs additional columns
#         )

#         # commit tables to db if not there yet, in any case, bind to engine
#         self.meta.create_all(self.engine, checkfirst=True)

#         if need_dummy_data:
#             self.__fill_with_dummy_data()

#     def __get_place_id(self, place: str):
#         stmt = select([self.places.c.place_id]).where(self.places.c.name == place)  #
#         stmt.compile()
#         query_result = [row for row in self.engine.connect().execute(stmt)]
#         if len(query_result) == 0:
#             return None
#         else:
#             return query_result[0][0]

#     def __insert_place(self, place: str):
#         stmt = insert(self.places).values(name=place)
#         stmt.compile()
#         self.engine.execute(stmt)
#         return self.__get_place_id(place)

#     def __get_data_id(self, other_data):
#         # returns last id right now
#         stmt = select([self.data.c.data_id])
#         stmt.compile()
#         query_result = self.engine.execute(stmt)
#         return list(query_result)[-1][0]

#     def __insert_data(
#         self,
#         name_de: str,
#         name_en: str,
#         assignee: str,
#         place_id: int,
#         desc_de: str = None,
#         desc_en: str = None,
#         insta: bool = False,
#         fb: bool = False,
#         nl: bool = False,
#         twitter: bool = False,
#         calendar: bool = False,
#         discord: bool = False,
#     ):
#         value_dict = {
#             "name_de": name_de,
#             "name_en": name_en,
#             "place_id": place_id,
#             "assignee": assignee,
#             "desc_de": desc_de,
#             "desc_en": desc_en,
#             "insta": insta,
#             "fb": fb,
#             "nl": nl,
#             "twitter": twitter,
#             "discord": discord,
#             "calendar": calendar,
#         }
#         # get sql statement
#         data_stmt = insert(self.data).values(value_dict)

#         # and execute on db
#         self.engine.execute(data_stmt)

#         # return id
#         return self.__get_data_id({})

#     def __get_event_id(self):
#         stmt = select([self.events.c.id])
#         result_query = self.engine.connect().execute(stmt)
#         return list(result_query)[-1][0]

#     def __insert_event(self, start: int, data_id: int, end: int = None):
#         # compile statement
#         events_stmt = insert(self.events).values(
#             {"start": start, "end": end, "data_id": data_id, "created": dt.now()}
#         )
#         # execute
#         self.engine.connect().execute(events_stmt)

#         return self.__get_event_id()

#     def __get_regularity_id(self, other_reg_data):
#         # incomplete should identify reg id base on other data
#         # right now returns last id
#         stmt = select([self.regularities.c.reg_id])
#         stmt.compile()
#         query_result = self.engine.execute(stmt)
#         return list(query_result)[-1][0]

#     def __insert_regularity(self, outdated: bool = False):
#         stmt = insert(self.regularities).values(outdated=outdated)
#         stmt.compile()
#         self.engine.execute(stmt)
#         return self.__get_regularity_id({})

#     def __fill_with_dummy_data(self):
#         # some templates
#         templates = [
#             {
#                 "name_de": "Queercafe",
#                 "name_en": "Queercafe",
#                 "assignee": "Jutta, BraBra",
#                 "nl": True,
#                 "place": "Online",
#             },
#             {
#                 "name_de": "Filmabend",
#                 "name_en": "movie night",
#                 "assignee": "Dirne",
#                 "insta": True,
#                 "place": "Online",
#             },
#         ]
#         reg_ids = []
#         for template in templates:
#             reg_ids.append(self.insert_new_template(**template))

#         # some reg events
#         for reg_id in reg_ids:
#             start = today()
#             start2 = start + relativedelta(days=+1)
#             end = start + relativedelta(days=+1)
#             self.insert_new_regular_event(reg_id, start=start.timestamp())
#             self.insert_new_regular_event(
#                 reg_id, start=start2.timestamp(), end=end.timestamp()
#             )

#         # a new event
#         self.insert_new_singular_event(
#             name_de="Mitgliederversammlung",
#             name_en="general meeting",
#             assignee="Annegreat",
#             start=(today() + relativedelta(months=+1)).timestamp(),
#         )

#         for table in [self.events, self.data, self.places, self.regularities]:
#             print("table:", table.fullname)
#             stmt = select([table]).compile()
#             for row in self.engine.execute(stmt):
#                 print(dict(row))

#     def insert_new_singular_event(
#         self,
#         name_de: str,
#         name_en: str,
#         assignee: str,
#         start: int,
#         end: int = None,
#         place: str = "Queerreferat",
#         desc_de: str = None,
#         desc_en: str = None,
#         insta: bool = False,
#         fb: bool = False,
#         nl: bool = False,
#         twitter: bool = False,
#         calendar: bool = False,
#         discord: bool = False,
#     ):
#         # get place identifier
#         if (place_id := self.__get_place_id(place)) is None:
#             place_id = self.__insert_place(place)

#         # fill data table
#         data_id = self.__insert_data(
#             name_de=name_de,
#             name_en=name_en,
#             assignee=assignee,
#             place_id=place_id,
#             desc_de=desc_de,
#             desc_en=desc_en,
#             insta=insta,
#             fb=fb,
#             nl=nl,
#             twitter=twitter,
#             calendar=calendar,
#             discord=discord,
#         )

#         event_id = self.__insert_event(start=start, data_id=data_id, end=end)
#         return event_id

#     def insert_new_template(
#         self,
#         name_de: str,
#         name_en: str,
#         assignee: str,
#         place: str = "Queerreferat",
#         desc_de: str = None,
#         desc_en: str = None,
#         insta: bool = False,
#         fb: bool = False,
#         nl: bool = False,
#         twitter: bool = False,
#         calendar: bool = False,
#         discord: bool = False,
#     ):
#         # arbitrary now but needs regularity params later
#         # get place identifier
#         if (place_id := self.__get_place_id(place)) is None:
#             self.__insert_place(place)
#             place_id = self.__get_place_id(place)

#         # get regularity params
#         reg_id = self.__insert_regularity(True)

#         # get data
#         data_id = self.__insert_data(
#             name_de=name_de,
#             name_en=name_en,
#             assignee=assignee,
#             place_id=place_id,
#             desc_de=desc_de,
#             desc_en=desc_en,
#             insta=insta,
#             fb=fb,
#             nl=nl,
#             twitter=twitter,
#             calendar=calendar,
#             discord=discord,
#         )
#         return data_id

#     def insert_new_regular_event(self, template_id: int, start: int, end: int = None):
#         event_id = self.__insert_event(start=start, data_id=template_id, end=end)
#         return event_id

#     def get_event(self, event_id: int):
#         stmt = (
#             select(
#                 [
#                     self.data.c.name_de,
#                     self.events.c.start,
#                     self.events.c.end,
#                     self.events.c.id,
#                     self.events.c.end,
#                     self.places.c.name,
#                 ]
#             )  # natural joins very difficult so this dirty solution
#             .where(self.events.c.id == event_id)
#             .where(self.events.c.data_id == self.data.c.data_id)
#             .where(self.data.c.place_id == self.places.c.place_id)
#             .compile()
#         )
#         for event in self.engine.connect().execute(stmt):
#             return dict(event)