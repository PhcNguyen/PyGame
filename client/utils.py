import os
import time
from modules.style import Colors



def spins(n: int) -> bool:
    try:
        term_size = os.get_terminal_size()
        space = ' ' * ((term_size.columns - 14) // 2)
        print(f"{Colors.white}\n" * ((term_size.lines - 3) // 2) + f"{space}╔══════════╗")
        
        for delay in [0.002 + 0.001 * i for i in range(99)]:
            print(f"{space}║ -> {Colors.yellow}{n%98+1:02d}{Colors.white} <- ║", end='\r')
            n += 1
            time.sleep(delay)

        print(f"\n{space}╚══════════╝\n")
        return True
    except:
        return False