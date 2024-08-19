from os import get_terminal_size
from sys import stdout

from modules.style import Colors



HOME = '''
╔══════════════════════════════════╗
║               HOME               ║
║                                  ║
║ 1.REGISTER - ĐĂNG KÝ             ║
║ 2.LOGIN - ĐĂNG NHẬP    0.EXIT    ║
╚══════════════════════════════════╝
'''

MENU = '''
╔══════════════════════════════════╗
║               MENU               ║
║ 1.SPINS                4.CODE    ║
║ 2.DICE                           ║
║ 3.BANKING COIN         0.EXIT    ║
╚══════════════════════════════════╝
'''

DICE = '''
╔══════════════════════════════════╗
║               DICE               ║
║                                  ║
║                                  ║
╚══════════════════════════════════╝
'''

SPINS = '''
╔══════════════════════════════════╗
║              SPINS               ║
║                                  ║
║                                  ║
╚══════════════════════════════════╝
'''

LOGIN = '''
╔══════════════════════════════════╗
║        LOGIN - ĐĂNG NHẬP         ║
║                                  ║
║                                  ║
╚══════════════════════════════════╝
'''

REGISTER = '''
╔══════════════════════════════════╗
║        REGISTER - ĐĂNG KÝ        ║
║                                  ║
║                                  ║
╚══════════════════════════════════╝
'''


def drawDivider() -> bool:
    try:
        terminal_size = get_terminal_size().columns
        stdout.write(f"{Colors.white}▂{Colors.red}▂" * (terminal_size // 2) + "\n")
        return True
    except Exception: return False



class App:
    @staticmethod
    def render_frame(frame: str) -> None:
        print(frame)
        drawDivider()

    @staticmethod
    def home(): App.render_frame(HOME)
    @staticmethod
    def menu(): App.render_frame(MENU)
    @staticmethod
    def dice(): App.render_frame(DICE)
    @staticmethod
    def spins(): App.render_frame(SPINS)
    @staticmethod
    def login(): App.render_frame(LOGIN)
    @staticmethod
    def register(): App.render_frame(REGISTER)