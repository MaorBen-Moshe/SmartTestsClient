from app import app, socket_handler, app_main_logger, config

if __name__ == '__main__':
    app_main_logger.info("Starting server...")
    socket_handler.socketio.run(app,
                                host=config.get_server_host(),
                                port=config.get_server_port(),
                                allow_unsafe_werkzeug=True)
