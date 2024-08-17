import socket
import threading

from queue import Queue
from typing import Union
from modules.system import System



class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host, self.port = host, int(port)
        self.server = socket.socket()
        self.data_queue: Union[Queue | list] = Queue()

    
    def process_data_queue(self) -> None:
        """Xử lý dữ liệu từ hàng đợi."""
        while True:
            address, data = self.data_queue.get()  # Lấy dữ liệu từ hàng đợi
            System.console(address, 'Green', f'Đang xử lý gói tin: {data.decode()}')
            self.data_queue.task_done()  # Đánh dấu dữ liệu đã được xử lý


    def handleClient(self, client: socket.socket, address) -> None:
        """Xử lý dữ liệu từ client."""
        try:
            while (data := client.recv(4096)):
                self.data_queue.append([address[0], data])
                System.console(address[0], 'Yellow', f'Gói tin: {len(data)/1024:.3f} KB')
        except Exception as error:
            System.console(address[0], 'Red', error)
        finally:
            client.close()
            System.console(address[0], 'Blue', 'Đã ngắt kết nối')


    def handleConnections(self) -> None:
        """Xử lý kết nối đến từ client."""
        while True:
            client, addr = self.server.accept()
            System.console(addr[0], 'Orange', 'Đã kết nối')
            threading.Thread(target=self.handleClient, args=(client, addr)).start()


    def listening(self) -> None:
        """Bắt đầu lắng nghe kết nối từ client."""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()

            System.console(f'{self.host}:{self.port}', 'Green', 'Máy chủ đang lắng nghe')
            threading.Thread(target=self.handleConnections).start()
        except socket.error:
            System.console(self.host, 'Red', 'Địa chỉ đã được sử dụng')
        except Exception as error:
            System.console(self.host, 'Red', error)