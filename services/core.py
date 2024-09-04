import socket
import threading
import json

from modules.system import System
from services import sqlite, algorithm
from services.utils import isEven, isCoinMessage


class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host, self.port = host, int(port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def handleClient(self, client: socket.socket, address) -> None:
        """Xử lý dữ liệu từ client."""
        try:
            while True:
                data = client.recv(4096)
                if not data:
                    break  # Ngắt kết nối khi không nhận được dữ liệu
                if isinstance(data, bytes):
                    data = data.decode().split('|')
                else:
                    data = data.split('|')
                
                System.console(f'Packets: {len(data)}B', 'Yellow', data)
                response = self.handleData(data)
                client.send(response)
        except Exception as e:
            System.console(address, 'Red', f'Error: {e}')
        finally:
            client.close()

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
            System.console(self.host, 'Red', f'Error: {error}')

    @staticmethod
    def handleData(data: list) -> bytes:
        """
        Xử lý dữ liệu và thực hiện các hành động dựa trên giá trị đầu tiên trong danh sách.

        :param data: Danh sách chứa các thành phần dữ liệu.
        :return: Chuỗi byte chứa thông báo kết quả của hành động đã thực hiện.
        """

        def response(
            status: bool, 
            msg: str, 
            number: int = None, 
            coin: int = None
        ) -> bytes:
            result = {
                'status': status,
                'msg': msg,
                'username': username,
                'password': password,
                **({ 'number': number } if number is not None else {}),
                **({ 'coin': coin } if coin is not None else {})
            }
            return json.dumps(result).encode()

        try:
            action = float(data[0])
            username = data[1]
            password = data[2]
        except (IndexError, ValueError):
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
                return response(True, "Đăng nhập thành công.", coin=sqlite.getCoin(username))
            return response(False, "Đăng nhập thất bại.")
        
        # Hành động 1.5: Xem số xu hiện có
        elif action == 1.5:
            return response(True, 'Xu hiện tại.', coin=sqlite.getCoin(username))
        
        # Hành động 2: Trò chơi chẵn lẻ và cập nhật xu
        elif action == 2:
            if len(data) < 5:
                return response(False, 'Dữ liệu không đầy đủ.')
            
            try:
                select = int(data[3])
                coin = int(data[4])
            except ValueError:
                return response(False, 'Dữ liệu không hợp lệ.')
            
            if not sqlite.checkCoin(username, coin):
                return response(False, 'Số xu không đủ.')

            number = algorithm.ratioNumber(0.6) if select == 1 else algorithm.ratioNumber(0.4)
            isNumberEven = isEven(number) if select == 1 else not isEven(number)

            if isNumberEven:
                sqlite.updateCoin(username, password, coin)  # Thắng
                return response(True, isCoinMessage(coin * 1.8, True), number)
            else:
                sqlite.updateCoin(username, password, -coin)  # Thua
                return response(True, isCoinMessage(coin, False), number)

        # Hành động 3: Trò chơi xúc xắc
        elif action == 3:
            if len(data) < 5:
                return response(False, 'Dữ liệu không đầy đủ.')

            try:
                select = int(data[3])
                coin = int(data[4])
            except ValueError:
                return response(False, 'Dữ liệu không hợp lệ.')
            
            total, icons = algorithm.rollDice()

            if not sqlite.checkCoin(username, coin):
                return response(False, 'Số xu không đủ.')

            if algorithm.checkDice(select, total):
                sqlite.updateCoin(username, password, coin)  # Thắng
                return response(True, isCoinMessage(coin * 1.8, True), [total, icons])
            else:
                sqlite.updateCoin(username, password, -coin)  # Thua
                return response(True, isCoinMessage(coin, False), [total, icons])

        # Trường hợp hành động không hợp lệ
        return response(False, 'Hành động không hợp lệ.')
