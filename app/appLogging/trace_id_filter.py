import logging

import flask


class TraceIdFilter(logging.Filter):
    def __init__(self, get_function):
        super().__init__()
        self.get_request_id = get_function

    def filter(self, record) -> bool:
        record.trace_id = self.get_request_id() if flask.has_request_context() else ''
        return True
