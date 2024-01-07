import time

from flask_socketio import SocketIO

from app.models.serializable_model import Serializable
from app.models.singleton_meta import SingletonMeta


class SocketHandler(metaclass=SingletonMeta):
    """A class that handles socket communication with the client."""

    __slots__ = [
        "_socketio",
        "_event_name",
        "_namespace",
        "_app",
    ]

    def __init__(self, app):
        """Initializes the socket handler with the Flask app and the socket parameters.

        Args:
            app: The Flask app to use for the socket communication.
        """
        self._socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
        self._event_name = "event-smart-analyze-progress"
        self._namespace = "/smart-analyze-progress"
        self._app = app

    @property
    def socketio(self):
        """Gets the SocketIO instance.

        Returns:
            SocketIO: The SocketIO instance.
        """
        return self._socketio

    @property
    def event_name(self):
        """Gets the event name for the socket communication.

        Returns:
            str: The event name.
        """
        return self._event_name

    @property
    def namespace(self):
        """Gets the namespace for the socket communication.

        Returns:
            str: The namespace.
        """
        return self._namespace

    def send_message(self, message, session_id):
        """Sends a message to the client using the socket.

        Args:
            message (str): The message to send.
            session_id (str): The session ID of the client.
        """
        self.socketio.emit(self.event_name,
                           SocketResponse(message=message, session_id=session_id).toJSON(),
                           namespace=self.namespace)


class SocketResponse(Serializable):
    """A class that represents a socket response with a message, a session ID, and a timestamp."""

    def __init__(self, message: str, session_id: str):
        """Initializes the socket response with the given message and session ID.

        Args:
            message (str): The message to send.
            session_id (str): The session ID of the client.
        """
        self._message = message
        self._session_id = session_id
        self._timestamp = time.strftime("%Y/%m/%d %H:%M:$S", time.localtime())

    @property
    def message(self):
        """Gets or sets the message of the socket response.

        Returns:
            str: The message of the socket response.
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of the socket response.

        Args:
            message (str): The message of the socket response.
        """
        self._message = message

    @property
    def session_id(self):
        """Gets or sets the session ID of the socket response.

        Returns:
            str: The session ID of the socket response.
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        """Sets the session ID of the socket response.

        Args:
            session_id (str): The session ID of the socket response.
        """
        self._session_id = session_id
