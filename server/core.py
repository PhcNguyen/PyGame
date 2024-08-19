import time
import socket
import threading


from server import sqlite, algorithm
from modules.system import System



def handleData(data: list) -> str:
    """
    Xử lý dữ liệu và thực hiện các hành động dựa trên giá trị đầu tiên trong danh sách.

    :param data: Danh sách chứa các thành phần dữ liệu.
    :return: Thông báo kết quả của hành động đã thực hiện.
    """

    action = data[0]
    username, password = data[1], data[2]

    if action == 0:
        # 0|nguyen098xx|127172
        if not username or not password:
            return False
        elif not sqlite.isUsernameExists(username):
            return False
        return sqlite.createAccount(username, password)
    elif action == 1:
        # 1|nguyen098xx|127172
        return sqlite.loginAccount(username, password)
    elif action == 2:
        # 2|nguyen098xx|127172|1 or 2
        number = algorithm.listNumber()


class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host, self.port = host, int(port)
        self.server = socket.socket()


    def handleClient(self, client: socket.socket, address) -> None:
        """Xử lý dữ liệu từ client."""
        try:
            while (data := client.recv(4096)):
                System.console(address[0], 'Yellow', f'Gói tin: {len(data)/1024:.3f} KB')
                if isinstance(data, bytes): data.decode().split('|')

                client.send(handleData(data).encode())  # Gửi phản hồi lại client

        except Exception as error:
            System.console(address[0], 'Red', error)
        finally:
            client.close()
            System.console(address[0], 'Blue', 'Đã ngắt kết nối')


    def handleConnections(self) -> None:
        """Xử lý kết nối đến từ client."""
        while True:
            client, addr = self.server.accept()
            threading.Thread(target=self.handleClient, args=(client, addr)).start()


    def listening(self) -> None:
        """Bắt đầu lắng nghe kết nối từ client."""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()

            System.console(f'{self.host}:{self.port}', 'Green', 'Máy chủ đang lắng nghe')
            self.handleConnections()
        except socket.error:
            System.console(self.host, 'Red', 'Địa chỉ đã được sử dụng')
        except Exception as error:
            System.console(self.host, 'Red', error)