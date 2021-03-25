from flask.views import MethodView
from flask import jsonify
from typing import Dict, Union
from .db import QueryManager


class EventView(MethodView):
    def __init__(self, db: QueryManager):
        self.db = db
        super(EventView, self).__init__()

    def get(self):
        results = self.db.get_all_events()
        return jsonify(results)

    def post(self, event_dict: Dict[str, Union[str, int, bool]]):
        raise NotImplementedError
