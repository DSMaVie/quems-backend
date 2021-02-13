from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    create_engine,
    MetaData,
    Table,
    ForeignKey,
)
from pathlib import Path
import os


class EventDatabase:
    def __init__(self, path_to_db: Path):
        self.path = path_to_db

        # load and wrap initialization vars
        verbosity = bool(os.getenv("DB_VERBOSITY", False))
        db_url = "sqlite:///" + str(path_to_db.resolve())

        # define engine and meta
        self.engine = create_engine(db_url, echo=verbosity)
        self.meta = MetaData()

        # define tables
        self.events = Table(
            "events",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("start", Integer, nullable=False),
            Column("end", Integer),
            Column("data_id", Integer, ForeignKey("data.id"), nullable=False),
            Column("last_edited", Integer, nullable=False),
        )
        self.data = Table(
            "data",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("place_id", Integer, ForeignKey("place.id")),
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
        )
        self.place = Table(
            "place",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("place", String, nullable=False, unique=True),
        )
        self.regularity = Table(
            "regularity",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("outdated", Boolean, nullable=False),  # needs additional columns
        )

        # commit tables to db if not there yet, else, bind to
        self.meta.create_all(self.engine, checkfirst=True)
