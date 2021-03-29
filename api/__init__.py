from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
from .db import QueryManager
from .event import EventView
import os

# create Flask app
api = Flask(__name__)
CORS(api)

# loading of env vars
load_dotenv(verbose=True)

# wrap env vars in objects if necessary
db_loc = Path(os.getenv("DB_LOCATION"))
db_name = os.getenv("DB_NAME")
db_path = (db_loc / db_name).resolve()

# load db manager
db = QueryManager(db_path)

# load views
event_requests = EventView.as_view("events", db=db)
api.add_url_rule("/events", view_func=event_requests)


### LEGACY
# @api.route("/templates", methods=["GET", "POST"])
# def templates():
#     results = db.get_all_events()
#     return jsonify(results)


# @api.route("/places", methods=["GET", "POST"])
# def places():
#     results = db.get_all_places()
#     return jsonify(results)
