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
║ 3.BANKING COIN         0.BACK    ║
╚══════════════════════════════════╝
'''

DICE = '''
╔══════════════════════════════════╗
║               DICE               ║
║                                  ║
║                                  ║
║                        0.BACK    ║
╚══════════════════════════════════╝
'''

SPINS = '''
╔══════════════════════════════════╗
║            SPINS x1.8            ║
║                                  ║
║ 1.ODD - Lẻ                       ║
║ 2.EVEN - Chẳn           0.BACK   ║
╚══════════════════════════════════╝
'''

LOGIN = '''
╔══════════════════════════════════╗
║        LOGIN - ĐĂNG NHẬP         ║
║                                  ║
║                         0.BACK   ║
╚══════════════════════════════════╝
'''

REGISTER = '''
╔══════════════════════════════════╗
║        REGISTER - ĐĂNG KÝ        ║
║                                  ║
║                         0.BACK   ║
╚══════════════════════════════════╝
'''


def drawDivider(terminal_size) -> bool:
    try:
        stdout.write(f"{Colors.white}▂{Colors.red}▂{Colors.white}" * (terminal_size // 2) + "\n")
        return True
    except Exception: return False



class App:
    @staticmethod
    def render_frame(frame: str) -> None:
        terminal_size = get_terminal_size().columns
        for line in frame.strip().split('\n'):
            left_padding = (terminal_size - len(line)) // 2
            print(' ' * left_padding + line)
        drawDivider(terminal_size)

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