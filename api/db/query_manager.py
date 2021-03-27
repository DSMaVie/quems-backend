from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from functools import wraps
from inspect import signature
from typing import Callable
from .schema import Event, Data, Place, Regularity, BaseTable
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

    def with_session(func: Callable):
        """wraps a session around the func

        Args:
            func (Callable): func needs as signature either
            (self, session, *args, **kwargs) or (session, *args, **kwargs).
        """

        @wraps(func)
        def wrapped_with_session(self, *args, **kwargs):
            with self.session.begin() as sess:
                if "self" in signature(func).parameters:
                    return func(self, sess, *args, **kwargs)
                else:
                    return func(sess, *args, **kwargs)

        return wrapped_with_session

    @with_session
    def add_singular_event(sess, *args, **kwargs):
        if (place_id := Place.get_id(sess, name=kwargs["place"])) is None:
            sess.add(Place(name=kwargs["place"]))
            place_id = Place.get_id(sess, name=kwargs["place"])

        data_kwargs = Data.drop_non_columns(kwargs)
        sess.add(Data(**data_kwargs, place_id=place_id))
        data_id = Data.get_id(sess, **data_kwargs)

        event_kwargs = Event.drop_non_columns(kwargs)
        sess.add(Event(**event_kwargs, data_id=data_id, created=dt.now()))
        event_id = Event.get_id(sess, **event_kwargs)
        return event_id

    @with_session
    def add_template(sess, *args, **kwargs):
        if (place_id := Place.get_id(sess, name=kwargs["place"])) is None:
            sess.add(Place(name=kwargs["place"]))
            place_id = Place.get_id(sess, name=kwargs["place"])

        sess.add(Regularity(outdated=False))
        reg_id = Regularity.get_id(sess, outdated=False)

        data_kwargs = Data.drop_non_columns(kwargs)
        sess.add(
            Data(**data_kwargs, place_id=place_id, reg_id=reg_id)
        )  # might need kwarg filtering
        data_id = Data.get_id(sess, **data_kwargs)
        return data_id

    @with_session
    def add_regular_event(sess, id, *args, **kwargs):
        sess.add(Event(data_id=id, **kwargs, created=dt.now()))

    @with_session
    def get_all_events(sess):
        stmt = select(Event)
        result = sess.execute(stmt).scalars()
        return [event.unpack() for event in result]

    @with_session
    def get_all_templates(sess):
        stmt = select(Data).where(Data.reg_id != None)
        result = sess.execute(stmt).scalars()
        return [data.unpack() for data in result]

    @with_session
    def get_all_places(sess):
        stmt = select(Place.name)
        result = sess.execute(stmt).scalars()
        return list(result)

    def __load_dummy_data(self):
        s1_id = self.add_singular_event(
            name_de="Mitgliederversammlung",
            start=dt.now() + relativedelta(days=+1),
            assignee="Vorstand",
            place="Queerreferat",
            desc_de="eine wilde Beschreibung taucht auf ...",
            nl=True,
            calendar=True,
        )
        s2_id = self.add_singular_event(
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