import time

from flask_socketio import SocketIO

from app.models.serializable_model import Serializable
from app.models.singleton_meta import SingletonMeta


class SocketHandler(metaclass=SingletonMeta):
    def __init__(self, app):
        self._socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
        self._event_name = "event-smart-analyze-progress"
        self._namespace = "/smart-analyze-progress"
        self._app = app

    @property
    def socketio(self):
        return self._socketio

    @property
    def event_name(self):
        return self._event_name

    @property
    def namespace(self):
        return self._namespace

    def send_message(self, message, session_id):
        self.socketio.emit(self.event_name,
                           SocketResponse(message=message, session_id=session_id).toJSON(),
                           namespace=self.namespace)


class SocketResponse(Serializable):
    def __init__(self, message: str, session_id: str):
        self._message = message
        self._session_id = session_id
        self._timestamp = time.strftime("%Y/%m/%d %H:%M:$S", time.localtime())

    @property
    def message(self):
        return self._message

    @property
    def session_id(self):
        return self._session_id
