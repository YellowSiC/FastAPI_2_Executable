import logging
import os
import sys
from multiprocessing import freeze_support

from uvicorn import Config, Server

from app import app

if __name__ == "__main__":
    freeze_support()
    try:
        if getattr(sys, "frozen", False):  # Überprüft, ob das Programm eingefroren ist
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
        log_file_path = os.path.join(application_path, "Serverlog", "server.log")
        log_dir = os.path.dirname(log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logging.basicConfig(filename=log_file_path, level=logging.INFO)
        config = Config(app=app, host="127.0.0.1", port=8000, log_config=None)
        server = Server(config)
        server.run()
    except KeyboardInterrupt:
        print("Unterbrochen")
        sys.exit(1)
