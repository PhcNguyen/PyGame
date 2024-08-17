import pathlib

from server.utils import localIP




BASE_DIR = pathlib.Path(__file__).resolve()
DEBUG = True


HOST = localIP()
PORT = 19000

print(BASE_DIR)