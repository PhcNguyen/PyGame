import os
import time
import socket
import pathlib
import requests
import threading
import subprocess

from queue import Queue
from typing import Union
from modules.core.system import System



class Github:
    start = time.time()
    version = (
        pathlib.Path(__file__).parent.joinpath('version').read_text().strip()
    )

    @staticmethod
    def connect(url: str | bytes) -> bool:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                System.console('Ping', 'Orange', f'Connect to "{url.split('//')[-1]}" successful')
                return True
            else:
                System.console('Ping', 'Red', f'Error: HTTP status code {response.status_code}')
                return False
        except Exception as e:
            System.console('Ping', 'Red', str(e))
            return False

    @staticmethod
    def command(command, message) -> None:
        try:
            subprocess.run(command, -1, None, None, -3, -3)
            System.console('GitHub', 'Blue', message)
        except FileNotFoundError:
            System.console('GitHub', 'Red', 'Git command not found')
            System.exit()
        except Exception as e:
            System.console('GitHub', 'Red', f'Error executing Git command: {e}')
            System.exit()

    @staticmethod
    def automatic() -> None:
        if not Github.connect('https://github.com'):
            System.exit()
        
        commands = [
                (['git', 'add', '.'], 'git add .'),
                (['git', 'commit', '-m', Github.version], f'git commit -m "{Github.version}"'),
                (['git', 'push', 'origin', 'main'], 'git push origin main')
        ]
        for command in commands:
            Github.command(command[0], command[-1])
        
        System.console(
            'Timer', 'Yellow', 
            f'Elapsed time for push: {(time.time() - Github.start):.2f} seconds'
        )



class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host, self.port = host, int(port)
        self.server = socket.socket()
        self.data_queue: Union[Queue | list] = Queue()

    
    def process_data_queue(self) -> None:
        """Xử lý dữ liệu từ hàng đợi."""
        while True:
            address, data = self.data_queue.get()  # Lấy dữ liệu từ hàng đợi
            # Xử lý dữ liệu (ví dụ: ghi vào file, phân tích, v.v.)
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