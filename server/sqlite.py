import pathlib
import sqlite3

from typing import Union


def sqlConnection() -> sqlite3.Connection:
    return sqlite3.connect(
        pathlib.Path(__file__).resolve().parent.parent / 'database' / 'user.sql'
    )


def createDatabase() -> bool:
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                coin INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        return True
    except: return False
    finally: conn.close()


def isUsernameExists(username: str) -> bool:
    """Kiểm tra xem username có tồn tại trong cơ sở dữ liệu hay không."""
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute('SELECT 1 FROM users WHERE username = ?', (username,))
        result = c.fetchone()  
        conn.close()
        # Trả về True nếu username đã tồn tại, False nếu không
        return result is not None
    except: return False

    
def createAccount(username: str, password: str) -> bool:
    """Tạo người dùng mới với 0 coin."""
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (username, password, coin)
            VALUES (?, ?, ?)
        ''', (username, password, 0))
        conn.commit()
        return True
    # Trả về False để chỉ lỗi khi tạo người dùng
    except sqlite3.IntegrityError: return False 
    finally: conn.close()
    


def loginAccount(username: str, password: str) -> Union[int | bool]:
    """Xác thực người dùng dựa trên username và password."""
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute('''
            SELECT uid FROM users WHERE username = ? AND password = ?
        ''', (username, password))
        result = c.fetchone()
        if result:
            return result[0] #coin
        return False
    except sqlite3.Error: return False
    finally: conn.close()


def updatePassword(username: str, old_password: str, new_password: str) -> bool:
    """Cập nhật mật khẩu của người dùng dựa trên username sau khi xác thực mật khẩu cũ."""
    try:
        conn = sqlConnection()
        c = conn.cursor()

        # Xác thực mật khẩu cũ
        c.execute('''
            SELECT password FROM users WHERE username = ?
        ''', (username,))
        result = c.fetchone()

        if result:
            stored_password = result[0]
            if stored_password == old_password:  # So sánh mật khẩu cũ
                # Cập nhật mật khẩu mới
                c.execute('''
                    UPDATE users SET password = ? WHERE username = ?
                ''', (new_password, username))
                
                if c.rowcount == 0:
                    conn.rollback()
                    return False
                conn.commit()
                return True
            else:
                return False  # Mật khẩu cũ không đúng
        else:
            return False  # Tên người dùng không tồn tại

    except sqlite3.Error: return False
    finally: conn.close()


def updateCoin(username: str, password: str, additional_coins: int) -> bool:
    """Cập nhật số xu của người dùng bằng cách cộng thêm số xu mới sau khi xác thực mật khẩu."""
    try:
        conn = sqlConnection()
        c = conn.cursor()

        # Xác thực mật khẩu
        c.execute('''
            SELECT password, coin FROM users WHERE username = ?
        ''', (username,))
        result = c.fetchone()

        if result:
            stored_password, current_coins = result
            if stored_password == password:  # So sánh mật khẩu
                new_coin_amount = current_coins + additional_coins
                c.execute('''
                    UPDATE users SET coin = ? WHERE username = ?
                ''', (new_coin_amount, username))
                conn.commit()
                return True
            else:
                return False  # Mật khẩu không đúng
        else:
            return False  # Tên người dùng không tồn tại
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()


def deleteUser(uid: int) -> bool:
    """Xóa người dùng dựa trên uid và trả về True nếu thành công, False nếu thất bại."""
    try:
        conn = sqlConnection()
        c = conn.cursor()
        c.execute('''
            DELETE FROM users WHERE uid = ?
        ''', (uid,))
        conn.commit()
        if c.rowcount > 0:
            return True
        else: return False
    except sqlite3.Error: return False 
    finally: conn.close()