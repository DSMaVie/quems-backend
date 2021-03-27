import os
from dataclasses import dataclass
from pathlib import Path

import pytest
from api.db.query_manager import QueryManager

test_db_loc = Path("data/testdb.sqlite").resolve()  # make fixture as well


@pytest.fixture(scope="session")
def query_manager():
    qm = QueryManager(test_db_loc)
    yield qm
    del qm
    os.remove(test_db_loc)


def test_query_manager_setup(query_manager):
    assert query_manager.engine.url.database == str(test_db_loc)
    for table in ["events", "data", "places", "regularities"]:
        assert table in query_manager.meta.tables


class TestAddQueries:
    def test_add_events(self, query_manager):
        pass

    def test_add_data(self, query_manager):
        pass