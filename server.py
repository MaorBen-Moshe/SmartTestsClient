from app import app, socket_handler


if __name__ == '__main__':
    socket_handler.socketio.run(app, host="0.0.0.0", port=5001, allow_unsafe_werkzeug=True)
