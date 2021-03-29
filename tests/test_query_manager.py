import os
from pathlib import Path
from dotenv import load_dotenv
import pytest
import json
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

load_dotenv()
TEST_DATA_LOC = Path(os.getenv("DB_TEST_DATA_FOLDER")).resolve()
DB_NAME = os.getenv("DB_NAME")


def test_query_manager_setup(query_manager):
    for table in ["events", "data", "places", "regularities"]:
        assert table in query_manager.meta.tables


class TestInsertions:
    def test_add_singular_event(self, dummy_event_file, query_manager):
        with open(dummy_event_file) as event_file:
            events = json.load(event_file)

        for event in events:
            event |= {
                "start": dt.now(),
                "end": dt.now() + relativedelta(hours=+2),
            }
            event_id = query_manager.add_singular_event(**event)

            assert type(event_id) == int

    def test_add_template(self, dummy_template_file, query_manager):
        with open(dummy_template_file) as template_file:
            templates = json.load(template_file)
        for template in templates:
            template_id = query_manager.add_template(**template)
            assert type(template_id) == int


class TestGetters:
    def test_get_all_events(self, dummy_event_file, query_manager):
        with open(dummy_event_file) as event_file:
            events = json.load(event_file)
        queried_events = query_manager.get_all_events()
        for event, query in zip(events, queried_events):
            # wont work with regulars
            if event["name_de"] == query["name_de"]:
                for key, value in event.items():
                    assert query[key] == value

    def test_get_all_templates(self, dummy_template_file, query_manager):
        with open(dummy_template_file) as template_file:
            templates = json.load(template_file)
        queried_templates = query_manager.get_all_templates()
        for template, query in zip(templates, queried_templates):
            if template["name_de"] == query["name_de"]:
                for key, value in template.items():
                    assert query[key] == value