from flask import Flask, jsonify
from dotenv import load_dotenv
from pathlib import Path
from query_manger import QueryManager

import os

# TODO: make own class
api = Flask(__name__)

env_path = Path("./dev.env")
env_verbose = True
load_dotenv(env_path, verbose=env_verbose)

# wrap env vars in objects if necessary
db_path = Path(os.getenv("DB_LOCATION"))

# load db and api sever
db = QueryManager(db_path)


@api.route("/")
def hello_world():
    return "Go away, World!"


@api.route("/events", methods=["GET", "POST"])
def events():
    results = db.get_all_events()
    return jsonify(results)


@api.route("/templates", methods=["GET", "POST"])
def templates():
    results = db.get_all_events()
    return jsonify(results)


@api.route("/places", methods=["GET", "POST"])
def places():
    results = db.get_all_places()
    return jsonify(results)


if __name__ == "__main__":
    # TODO: make argparsable
    # load env vars
    api.run()
