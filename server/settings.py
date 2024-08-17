import pathlib

from server.utils import localIP



DEBUG = True

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / 'database' / 'user.sql'


HOST = localIP()
PORT = 19000