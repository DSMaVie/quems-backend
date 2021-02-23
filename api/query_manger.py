from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from schema import Event, Data, Place, Regularity, BaseTable
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import os


class QueryManager:
    def __init__(self, path_to_db: Path):
        # load and wrap initialization vars
        debug = bool(os.getenv("DB_DEBUG", False))
        need_dummy_data = bool(os.getenv("DB_FILL_WITH_DUMMIES", False))

        # define engine and meta
        db_url = "sqlite:///" + str(path_to_db.resolve())
        self.engine = create_engine(db_url, echo=debug)
        self.meta = BaseTable.metadata
        self.session = sessionmaker(self.engine, future=True)

        self.meta.create_all(bind=self.engine)

        if need_dummy_data:
            self.__load_dummy_data()

    def add_singular_event(self, *args, **kwargs):
        with self.session.begin() as sess:
            if (place_id := Place.get_id(sess, kwargs["place"])) is None:
                sess.add(Place(name=place_id))
                place_id = Place.get_id(sess, kwargs["place"])

            sess.add(Data(**kwargs, place_id=place_id))  # might need kwarg filtering
            data_id = Data.get_id(sess, **kwargs)

            sess.add(Event(**kwargs, data_id=data_id, created=dt.now()))
            event_id = Event.get_id(sess, **kwargs)
            return event_id

    def add_template(self, *args, **kwargs):
        with self.session.begin() as sess:
            if (place_id := Place.get_id(sess, name=kwargs["place"])) is None:
                sess.add(Place(name=place_id))
                place_id = Place.get_id(sess, name=kwargs["place"])

            sess.add(Regularity(outdated=False))
            reg_id = Regularity.get_id(sess, outdated=False)
            sess.add(
                Data(**kwargs, place_id=place_id, reg_id=reg_id)
            )  # might need kwarg filtering
            data_id = Data.get_id(sess, **kwargs)
            return data_id

    def add_regular_event(self, id, *args, **kwargs):
        with self.session.begin() as sess:
            sess.add(Event(data_id=id, **kwargs, created=dt.now()))

    def __load_dummy_data(self):
        self.add_singular_event(
            name_de="Mitgliederversammlung",
            start=dt.now() + relativedelta(days=+1),
            assignee="Vorstand",
            place="Queerreferat",
            desc_de="eine wilde Beschreibung taucht auf ...",
            nl=True,
            calendar=True,
        )
        self.add_singular_event(
            name_de="Workshop: ist queeres Python anders?",
            name_en="Workshop: is queer python different?",
            start=dt.now() + relativedelta(days=+2),
            end=dt.now() + relativedelta(days=+2, hours=+2),
            assignee="Alex",
            place="Queerreferat",
            desc_de="In diesem Workshop gehen wir der Frage nach, ob Python, dass von queeren Menschen geschrieben wird linguistisch different von hetero=python ist.",
            insta=True,
            nl=True,
            calendar=True,
        )
        cafe_id = self.add_template(
            name_de="Queercafe",
            name_en="Queercafe",
            desc_de="Kaffee und Kuchen",
            assignee="Helga",
            place="Online",
            insta=True,
            discord=True,
        )
        bm_id = self.add_template(
            name_de="Vorstandssitzung",
            desc_de="geschlossene Sitzung, nur fuer Vorstandsmitglieder",
            place="Bei Jutta",
            assignee="Jutta",
        )
        for index, id in enumerate([cafe_id, bm_id]):
            self.add_regular_event(
                id,
                start=dt.now() + relativedelta(days=(index + 1) * 7),
                end=dt.now() + relativedelta(days=(index + 1) * 7, hours=+2),
            )
            self.add_regular_event(
                id,
                start=dt.now() + relativedelta(days=(index + 2) * 7),
                end=dt.now() + relativedelta(days=(index + 2) * 7, hours=+2),
            )

    def get_all_events(self):
        with self.session.begin() as sess:
            stmt = (
                select(Event)
                .join(Data, Data.id == Event.data_id)
                .join(Place, Place.id == Data.place_id)
            )
            result = sess.execute(stmt).all()
            return [dict(row) for row in result]

    def get_all_templates(self):
        with self.session.begin() as sess:
            stmt = (
                select(Data)
                .join(Place, Place.id == Data.place_id)
                .join(Regularity, Regularity.id == Data.reg_id)
            )
            result = sess.execute(stmt)
            return [dict(row) for row in result]

    def get_all_places(self):
        with self.session.begin() as sess:
            stmt = select(Place.name)
            result = sess.execute(stmt)
            return [dict(row) for row in result]