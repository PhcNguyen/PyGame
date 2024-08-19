import socket


class Client:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.client = socket.socket()

    def connect(self) -> None:
        """Kết nối tới server."""
        try:
            self.client.connect((self.host, self.port))
            print(f"Đã kết nối tới {self.host}:{self.port}")
        except Exception as error:
            print(f"Lỗi kết nối tới server: {error}")

    def send_data(self, message: str) -> None:
        """Gửi dữ liệu tới server và nhận phản hồi."""
        try:
            self.client.send(message.encode())  # Gửi dữ liệu
            print(f"Đã gửi: {message}")

            response = self.client.recv(4096).decode()  # Nhận phản hồi từ server
            print(f"Phản hồi từ server: {response}")

        except Exception as error:
            print(f"Lỗi khi gửi dữ liệu: {error}")
        finally:
            self.client.close()
            print("Đã đóng kết nối với server")

if __name__ == "__main__":
    # Thông tin server (cần thay đổi nếu server chạy ở địa chỉ và cổng khác)
    host = "127.0.0.1"  # Địa chỉ IP của server (localhost)
    port = 12345         # Cổng của server

    # Khởi tạo client và kết nối tới server
    client = Client(host, port)
    client.connect()

    # Gửi một chuỗi dữ liệu từ người dùng nhập vào
    message = input("Nhập thông điệp để gửi tới server: ")
    client.send_data(message)
