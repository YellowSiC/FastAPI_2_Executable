import logging
from multiprocessing import freeze_support

from uvicorn import Config, Server

from app import app

if __name__ == "__main__":
    freeze_support()
    logging.basicConfig(filename="server.log", level=logging.INFO)
    config = Config(app=app, host="127.0.0.1", port=8000, log_config=None)
    server = Server(config)
    server.run()
