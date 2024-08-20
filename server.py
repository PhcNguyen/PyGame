from services.core import Server
from services.settings import HOST, PORT
from services.sqlite import updateCoin

#updateCoin('admin', '123', 1000000000)

Server(HOST, PORT).listening()