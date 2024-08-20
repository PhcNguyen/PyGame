import os
import time
from modules.style import Colors


term_size = os.get_terminal_size()
space = ' ' * ((term_size.columns - 14) // 2)


def spins(n: int) -> bool:
    try:
        print('\n' + f"{Colors.white}" * ((term_size.lines - 3) // 2) + f"{space}╔══════════╗")
        for delay in [0.002 + 0.001 * i for i in range(99)]:
            print(f"{space}║ -> {Colors.yellow}{n%98+1:02d}{Colors.white} <- ║", end='\r')
            n += 1
            time.sleep(delay)
        print(f"\n{space}╚══════════╝\n")
        return True
    except: return False


def displayMessage(message):
    print(f'{Colors.red}{" "*5}{message}{Colors.white}' if message else '\n')


def dice(x: str) -> bool:
    try:
        print('\n' + f"{Colors.white}" * ((term_size.lines - 3) // 2) + f"{space}╔═══════════╗")
        print(f"{space}║ -> {Colors.yellow}{''.join(x)}{Colors.white} <- ║")
        print(f"{space}╚═══════════╝\n")
        return True
    except: return False