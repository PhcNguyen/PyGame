import socket
import sqlite3


def localIP() -> str:
    # Create a dummy connection to determine the local IP without sending data
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def create_database():
    # Kết nối đến cơ sở dữ liệu (tạo mới nếu chưa tồn tại)
    conn = sqlite3.connect('database/user.sql')
    
    # Tạo đối tượng cursor để thực thi các câu lệnh SQL
    c = conn.cursor()
    
    # Tạo bảng với các trường uid, username, password, coin
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            coin INTEGER DEFAULT 0
        )
    ''')
    
    # Cam kết các thay đổi và đóng kết nối
    conn.commit()
    conn.close()
    print("Database and table created successfully.")


create_database()
