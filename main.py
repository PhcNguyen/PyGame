from services.core import Server
from services.settings import HOST, PORT


Server(HOST, PORT).listening()