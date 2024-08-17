import sqlite3

from typing import Union
from server.settings import DATABASE_PATH



def sqlConnection():
    return sqlite3.connect(DATABASE_PATH)


def createUid(username: str, password: str, coin: int) -> bool:
    """Tạo người dùng mới và trả về uid của người dùng đó."""
    conn = sqlConnection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (username, password, coin)
            VALUES (?, ?, ?)
        ''', (username, password, coin))
        # Cam kết thay đổi
        conn.commit()
    
    except sqlite3.IntegrityError as e:
        return False # Trả về False để chỉ lỗi khi tạo người dùng
    finally:
        conn.close()
    return True


def login(username: str, password: str) -> Union[int | bool]:
    """Xác thực người dùng dựa trên username và password."""
    conn = sqlConnection()
    try:
        c = conn.cursor()
        c.execute('''
            SELECT uid FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))
        
        # Lấy kết quả truy vấn
        result = c.fetchone()

        if result:
            coin = result[0]
            return coin
        else:
            return False
    
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()


def updatePassword(username: str, new_password: str) -> bool:
    """Cập nhật mật khẩu của người dùng dựa trên username."""
    conn = sqlConnection()
    try:
        c = conn.cursor()
        c.execute('''
            UPDATE users
            SET password = ?
            WHERE username = ?
        ''', (new_password, username))
        
        # Kiểm tra số hàng đã bị ảnh hưởng để xác định thành công
        if c.rowcount == 0:
            conn.rollback()
            return False
        
        conn.commit()
        return True
    
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()


def updateCoin(username: str, additional_coins: int) -> bool:
    """Cập nhật số xu của người dùng bằng cách cộng thêm số xu mới."""
    conn = sqlConnection()
    try:
        c = conn.cursor()
        c.execute('''
            SELECT coin FROM users
            WHERE username = ?
        ''', (username,))
        
        result = c.fetchone()
        
        if result:
            current_coins = result[0]
            new_coin_amount = current_coins + additional_coins
            
            # Cập nhật số xu mới vào cơ sở dữ liệu
            c.execute('''
                UPDATE users
                SET coin = ?
                WHERE username = ?
            ''', (new_coin_amount, username))
            
            conn.commit()
            return True
        else:
            return False
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()


def deleteUser(uid: int) -> bool:
    """Xóa người dùng dựa trên uid và trả về True nếu thành công, False nếu thất bại."""
    conn = sqlConnection()
    try:
        c = conn.cursor()
        c.execute('''
            DELETE FROM users
            WHERE uid = ?
        ''', (uid,))
        
        # Cam kết thay đổi
        conn.commit()
        
        # Kiểm tra số hàng bị ảnh hưởng để xác định thành công
        if c.rowcount > 0:
            return True
        return False
    except sqlite3.Error as e:
        return False 
    finally:
        conn.close()