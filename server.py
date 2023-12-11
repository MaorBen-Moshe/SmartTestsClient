from app import app, socket_handler, app_main_logger

if __name__ == '__main__':
    app_main_logger.info("Starting server...")
    socket_handler.socketio.run(app, host="0.0.0.0", port=5001, allow_unsafe_werkzeug=True)
