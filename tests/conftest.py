from pathlib import Path
from dotenv import load_dotenv
import pytest
from api.db.query_manager import QueryManager
import os

load_dotenv()
DB_NAME = os.getenv("DB_NAME")


@pytest.fixture
def dummy_template_file(shared_datadir):
    return shared_datadir / "templates.json"


@pytest.fixture
def dummy_event_file(shared_datadir):
    return shared_datadir / "events.json"


@pytest.fixture(scope="session", autouse=True)
def query_manager(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("tmp_db")
    qm = QueryManager(db_path / DB_NAME)
    return qm
