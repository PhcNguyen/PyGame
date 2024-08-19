import socket
import json


class Client:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def serverConnect(self) -> (bool | Exception):
        """Kết nối tới server."""
        try:
            self.client.connect((self.host, self.port))
            return True
        except Exception as error: return error

    def submitData(self, message: str) -> (bool | str):
        """Gửi dữ liệu tới server và nhận phản hồi."""
        try:
            self.client.send(message.encode())  # Gửi dữ liệu
            return json.loads(self.client.recv(4096).decode()) 
        except Exception: return False
    
    def closeConnection(self) -> (bool | Exception):
        try:
            self.client.close()
            return True
        except Exception as error: return error