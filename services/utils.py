from modules.style import Colors


def isEven(number: int) -> bool:
    '''
    Kiểm tra xem số có phải là số chẵn không.
    
    Parameters:
    - number (int): Số cần kiểm tra.

    Returns:
    - bool: True nếu là số chẵn, False nếu là số lẻ.
    '''
    return number % 2 == 0


def isCoinMessage(coin: int, is_win: bool) -> str:
    """
    Kiểm tra số xu và trả về thông báo thắng hoặc thua tùy thuộc vào giá trị của coin.
    
    :param coin: Số xu được cộng hoặc trừ.
    :param is_win: Biến boolean để xác định là thắng hay thua.
    :return: Thông báo tùy thuộc vào giá trị của coin và kết quả thắng/thua.
    """
    action = "được cộng" if is_win else "bị trừ"
    result = "Thắng!" if is_win else "Thua!"
    extra = " Chúc mừng bạn!" if is_win else " Cố gắng lần sau!"
    # Tạo thông báo cuối cùng
    return f"{result} Bạn {action} {coin:,} xu.{extra}"