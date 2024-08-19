import time
import socket
import threading

from modules.system import System

from services import sqlite, algorithm
from services.utils import isEven, isCoinMessage



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



def handleData(data: list) -> dict:
    """
    Xử lý dữ liệu và thực hiện các hành động dựa trên giá trị đầu tiên trong danh sách.

    :param data: Danh sách chứa các thành phần dữ liệu.
    :return: Từ điển chứa thông báo kết quả của hành động đã thực hiện.
    """
    # Hàm phụ để trả về thông báo với status
    def response(status: bool, msg: str) -> dict:
        return {'status': status, 'msg': msg}

    # Kiểm tra cấu trúc dữ liệu đầu vào
    try:
        action = data[0]
        username, password = data[1], data[2]
    except (IndexError, TypeError):
        return response(False, 'Hành động không hợp lệ.')

    # Hành động 0: Tạo tài khoản
    if action == 0:
        if not username or not password:
            return response(False, 'Tên người dùng hoặc mật khẩu không hợp lệ.')
        if sqlite.isUsernameExists(username):
            return response(False, "Tên người dùng đã tồn tại.")
        return response(sqlite.createAccount(username, password), "Tạo tài khoản thành công.")
    
    # Hành động 1: Đăng nhập
    elif action == 1:
        return response(sqlite.loginAccount(username, password), "Đăng nhập thành công.")

    # Hành động 2: Trò chơi chẵn lẻ và cập nhật xu
    elif action == 2:
        if len(data) < 5:
            return response(False, 'Dữ liệu không đầy đủ.')

        coin = data[4]
        if not sqlite.checkCoin(username, coin):
            return response(False, 'Số xu không đủ.')

        number = algorithm.listNumber(0.7) if data[3] == 1 else algorithm.listNumber(0.3)
        isNumberEven = isEven(number) if data[3] == 1 else not isEven(number)

        if isNumberEven:
            sqlite.updateCoin(username, password, coin)  # Thắng
            return response(True, isCoinMessage(coin, True))
        else:
            sqlite.updateCoin(username, password, -coin)  # Thua
            return response(False, isCoinMessage(coin, False))

    # Trường hợp hành động không hợp lệ
    return response(False, 'Hành động không hợp lệ.')


