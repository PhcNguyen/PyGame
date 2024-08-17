import os
import time
from modules.core.style import Colors



def spins(number) -> bool:
    try:
        term_size = os.get_terminal_size()

        padding_left = (term_size.columns - 14) // 2
        padding_top = (term_size.lines - 3) // 2
        space = ' ' * padding_left

        print(f"{Colors.white}\n" * padding_top + f"{space}╔══════════╗")
        
        delay = 0.002
        while delay < 0.1:
            number = (number % 98) + 1
            print(
                f"{{}}║ -> {{}}{number:02d}{{}} <- ║".format(
                    space, Colors.yellow, Colors.white
                ), end='\r'
            )
            time.sleep(delay)
            delay += 0.001
        
        print(f"\n{space}╚══════════╝\n")
        return True
    except KeyError:
        return False