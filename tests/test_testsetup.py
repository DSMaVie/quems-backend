import os
from pathlib import Path
from dotenv import load_dotenv
import pytest
import json

load_dotenv()
DB_NAME = os.getenv("DB_NAME")


def test_dummy_events(dummy_event_file):
    with dummy_event_file.open() as event_file:
        events = json.load(event_file)

    mandatory_keys = {"name_de", "assignee"}
    for event in events:
        assert mandatory_keys.issubset(event.keys())


def test_dummy_templates(dummy_template_file):
    with dummy_template_file.open() as template_file:
        templates = json.load(template_file)

    mandatory_keys = {"name_de", "assignee"}
    for template in templates:
        assert mandatory_keys.issubset(template.keys())
