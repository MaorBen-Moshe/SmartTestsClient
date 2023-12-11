import time

from flask_socketio import SocketIO

from app.models.singleton_meta import SingletonMeta


class SocketHandler(metaclass=SingletonMeta):
    def __init__(self, app):
        self._socketio = SocketIO(app, cors_allowed_origins="*")
        self._internal_event_name = "internal_smart-analyze-progress"
        self._namespace = "/smart-analyze-progress"
        self._app = app

    @property
    def socketio(self):
        return self._socketio

    @property
    def internal_event_name(self):
        return self._internal_event_name

    @property
    def namespace(self):
        return self._namespace

    def send_message(self, message, session_id):
        with self._app.app_context():
            self.socketio.emit(self._internal_event_name,
                               {
                                   "message": message,
                                   "time": time.strftime("%Y/%m/%d %H:%M:$S", time.localtime()),
                                   "session_id": session_id
                               },
                               namespace=self._namespace)
