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
                if isinstance(data, bytes): data = data.decode().split('|')
                else: data.split('|')
                System.console(f'Packets: {len(data[1])}B', 'Yellow', data)
                client.send(handleData(data))  # Gửi phản hồi lại client

        except Exception as error:
            System.console(address[0], 'Red', error)
        '''
        finally:
            client.close()
            System.console(address[0], 'Blue', 'Đã ngắt kết nối')
        '''


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



def handleData(data: list) -> bytes:
    """
    Xử lý dữ liệu và thực hiện các hành động dựa trên giá trị đầu tiên trong danh sách.

    :param data: Danh sách chứa các thành phần dữ liệu.
    :return: Chuỗi byte chứa thông báo kết quả của hành động đã thực hiện.
    """
    # Hàm phụ để trả về thông báo với status dưới dạng chuỗi byte
    def response(
        status: bool, msg: str, 
        number: int = None, coin: int = None
    ) -> bytes:
        result = {
            'status': status, 'msg': msg, 
            'username': username, 'password': password
        }
        if number is not None:
            result['number'] = number
        if coin is not None:
            result['coin'] = coin
        # Chuyển đổi từ điển thành chuỗi JSON và sau đó encode thành bytes
        import json
        return json.dumps(result).encode()

    # Kiểm tra cấu trúc dữ liệu đầu vào
    try:
        action: int   = int(data[0])
        username: str = data[1]
        password: str = data[2]
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
        if sqlite.loginAccount(username, password):
            return response(
                True, "Đăng nhập thành công.", 
                coin = sqlite.getCoin(username)
            )
        return response(False, "Đăng nhập thất bại.")

    # Hành động 2: Trò chơi chẵn lẻ và cập nhật xu
    elif action == 2:
        if len(data) < 5:
            return response(False, 'Dữ liệu không đầy đủ.')
        
        select = int(data[3])
        coin = int(data[4])

        if not sqlite.checkCoin(username, coin):
            return response(False, 'Số xu không đủ.')

        number = algorithm.ratioNumber(0.7) if select == 1 else algorithm.ratioNumber(0.3)
        isNumberEven = isEven(number) if select == 1 else not isEven(number)

        if isNumberEven:
            sqlite.updateCoin(username, password, coin)  # Thắng
            return response(True, isCoinMessage(coin, True), number)
        else:
            sqlite.updateCoin(username, password, -coin)  # Thua
            return response(False, isCoinMessage(coin, False), number)

    # Trường hợp hành động không hợp lệ
    return response(False, 'Hành động không hợp lệ.')