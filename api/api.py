from flask import Flask, jsonify
from dotenv import load_dotenv
from pathlib import Path
from database import EventDatabase

import os

# TODO: make own class
api = Flask(__name__)

env_path = Path("./dev.env")
env_verbose = True
load_dotenv(env_path, verbose=env_verbose)

# wrap env vars in objects if necessary
db_path = Path(os.getenv("DB_LOCATION"))

# load db and api sever
db = EventDatabase(db_path)


@api.route("/")
def hello_world():
    return "Go away, World!"


@api.route("/events", methods=["GET", "POST"])
def events():
    results = []
    for i in range(4):
        results.append(db.get_event(i + 1))
    return jsonify(results)


if __name__ == "__main__":
    # TODO: make argparsable
    # load env vars
    api.run()
