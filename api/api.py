from flask import Flask
from dotenv import load_dotenv
from pathlib import Path
from database import EventDatabase

import os

# TODO: make own class
api = Flask(__name__)


@api.route("/")
def hello_world():
    return "Go away, World!"


if __name__ == "__main__":
    # TODO: make argparsable
    # load env vars
    env_path = Path("./dev.env")
    env_verbose = True
    load_dotenv(env_path, verbose=env_verbose)

    # wrap env vars in objects if necessary
    db_path = Path(os.getenv("DB_LOCATION"))

    # load db and api sever
    db = EventDatabase(db_path)
    api.run()
