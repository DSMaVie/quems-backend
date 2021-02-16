from sqlalchemy import *
from pathlib import Path
import datetime as dt
import os


class EventDatabase:
    def __init__(self, path_to_db: Path):
        self.path = path_to_db

        # load and wrap initialization vars
        debug = bool(os.getenv("DB_DEBUG", False))
        db_url = "sqlite:///" + str(path_to_db.resolve())

        # define engine and meta
        self.engine = create_engine(db_url, echo=debug)
        self.meta = MetaData()

        # define tables
        self.events = Table(
            "events",
            self.meta,
            Column(
                "id", Integer, primary_key=True
            ),  # if not explicitly set is autoincremented
            Column("start", Integer, nullable=False),
            Column("end", Integer),
            Column("data_id", Integer, ForeignKey("data.id"), nullable=False),
            Column("created", Integer, nullable=False),
            Column("last_edited", Integer),
        )
        self.data = Table(
            "data",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("place_id", Integer, ForeignKey("place.id"), nullable=False),
            Column("reg_id", Integer, ForeignKey("regularity.id")),
            Column("name_de", String, nullable=False),
            Column("name_en", String, nullable=False),
            Column("assignee", String, nullable=False),
            Column("desc_de", String),
            Column("desc_de", String),
            Column("fb", Boolean, nullable=False),
            Column("insta", Boolean, nullable=False),
            Column("twitter", Boolean, nullable=False),
            Column("discord", Boolean, nullable=False),
            Column("nl", Boolean, nullable=False),
            Column("calendar", Boolean, nullable=False),
        )
        self.places = Table(
            "place",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("place", String, nullable=False, unique=True),
        )
        self.regularities = Table(
            "regularity",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("outdated", Boolean, nullable=False),  # needs additional columns
        )

        # commit tables to db if not there yet, in any case, bind to engine
        self.meta.create_all(self.engine, checkfirst=True)

        if debug:
            self.__fill_with_dummy_data()

    def __get_place_id(self, place: str):
        stmt = select(self.places.id).where(self.places.name == place)
        stmt.compile()
        query_result = [row for row in self.engine.connect().execute(stmt)]
        if len(query_result) == 0:
            return None
        else:
            return query_result[0]

    def __insert_place(self, place: str):
        stmt = insert(self.places).values(place=place).returning(self.places.id)
        stmt.compile()
        with self.engine.connect() as conn:
            new_id = conn.execute((stmt))[0]
            conn.commit()
        return new_id

    def __insert_data(
        self,
        name_de: str,
        name_en: str,
        assignee: str,
        place_id: int,
        desc_de: str = None,
        desc_en: str = None,
        insta: bool = False,
        fb: bool = False,
        nl: bool = False,
        twitter: bool = False,
        calendar: bool = False,
        discord: bool = False,
    ):

        # get sql statement
        data_stmt = (
            insert(self.data)
            .values(
                {
                    "name_de": name_de,
                    "name_en": name_en,
                    "place_id": place_id,
                    "assignee": assignee,
                    "desc_de": desc_de,
                    "desc_en": desc_en,
                    "insta": insta,
                    "fb": fb,
                    "nl": nl,
                    "twitter": twitter,
                    "discord": discord,
                    "calendar": calendar,
                }
            )
            .returning(self.data.id)
        )

        # and execute on db
        with self.engine.connect() as conn:
            new_id = conn.execute(data_stmt)[0]
            conn.commit()

        # return id
        return new_id

    def __insert_event(self, start: int, data_id: int, end: int = None):
        # compile statement
        events_stmt = (
            insert(events)
            .values(
                {"start": start, "end": end, "data_id": data_id, "created": dt.now()}
            )
            .returning(self.event.id)
        )
        # execute
        with self.engine.connect() as conn:
            new_id = conn.execute(events_stmt)[0]
            conn.commit()
        return new_id

    def __insert_regularity(self, outdated: bool = False):
        stmt = (
            insert(self.regularities)
            .values(outdated=outdated)
            .returning(self.regularities.id)
        )
        stmt.compile()
        with self.engine.connect() as conn:
            new_id = conn.execute((stmt))[0]
            conn.commit()
        return new_id

    def __fill_with_dummy_data(self):
        # some templates
        templates = [
            {
                "name_de": "Queercafe",
                "name_en": "Queercafe",
                "assignee": "Jutta, BraBra",
                "nl": True,
                "place": "Online",
            },
            {
                "name_de": "Filmabend",
                "name_en": "movie night",
                "assignee": "Dirne",
                "insta": True,
                "place": "Online",
            },
        ]
        reg_ids = []
        for template in templates:
            reg_ids.push(self.insert_new_template(**template))

        # some reg events
        for reg_id in reg_ids:
            start = dt.today()
            start2 = start + dt.timedelta(days=1)
            end = start + dt.timedelta(days=1)
            self.insert_new_regular_event(reg_id, start=start.timestamp())
            self.insert_new_regular_event(
                reg_id, start=start2.timestamp(), end=end.timestamp()
            )

        # a new event
        self.insert_new_singular_event(
            name_de="Mitgliederversammlung",
            name_en="general meeting",
            start=(dt.today() + dt.timedelta(months=1)).timestamp(),
        )
        raise NotImplementedError

    def insert_new_singular_event(
        self,
        name_de: str,
        name_en: str,
        assignee: str,
        start: int,
        end: int = None,
        place: str = "Queerreferat",
        desc_de: str = None,
        desc_en: str = None,
        insta: bool = False,
        fb: bool = False,
        nl: bool = False,
        twitter: bool = False,
        calendar: bool = False,
        discord: bool = False,
    ):
        # get place identifier
        if (place_id := self.__get_place_id(place)) is None:
            place_id = self.__insert_place(place)

        # fill data table
        data_id = self.__insert_data(
            name_de=name_de,
            name_en=name_en,
            assignee=assignee,
            place_id=place_id,
            desc_de=desc_de,
            desc_en=desc_en,
            insta=insta,
            fb=fb,
            nl=nl,
            twitter=twitter,
            calendar=calendar,
            discord=discord,
        )

        event_id = self.__insert_event(start=start, data_id=data_id, end=end)
        return event_id

    def insert_new_template(
        self,
        name_de: str,
        name_en: str,
        assignee: str,
        place: str = "Queerreferat",
        desc_de: str = None,
        desc_en: str = None,
        insta: bool = False,
        fb: bool = False,
        nl: bool = False,
        twitter: bool = False,
        calendar: bool = False,
        discord: bool = False,
    ):
        # arbitrary now but needs regularity params later
        # get place identifier
        if (place_id := self.__get_place_id(place)) is None:
            self.__insert_place(place)
            place_id = self.__get_place_id(place)

        # get regularity params
        reg_id = self.__insert_regularity(True)

        # get data
        data_id = self.__insert_data(
            name_de=name_de,
            name_en=name_en,
            assignee=assignee,
            place_id=place_id,
            desc_de=desc_de,
            desc_en=desc_en,
            insta=insta,
            fb=fb,
            nl=nl,
            twitter=twitter,
            calendar=calendar,
            discord=discord,
        )
        return data_id

    def insert_new_regular_event(self, template_id: int, start: int, end: int = None):
        event_id = self.__insert_event(start=start, data_id=template_id, end=end)
        return event_id