from flask import Flask

api = Flask(__name__)


@api.route("/")
def hello_world():
    return "Go away, World!"


if __name__ == "__main__":
    api.run()
