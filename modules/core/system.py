import sys
import time
import os.path

from typing import NoReturn
from modules.core.style import Colors
from modules.core.utils import FRAMES, MESSAGE



class System:
    """
    6 functions: 
    - clear()   |   Clears the terminal screen
    - command() |   Executes a system command
    - reset()   |   Resets the Python script by re-executing it
    - exit()    |   Exits the Python script
    - console() |   Prints a formatted message to the console
    - sleep()   |   Shows a countdown with a specified number of frames
    """
    Windows = os.name == 'nt'

    @staticmethod
    def init() -> int:
        os.system('')

    @staticmethod
    def clear() -> int:
        return os.system(
            "cls" if System.Windows else "clear"
        )
        
    @staticmethod
    def command(command: str) -> int:
        return os.system(command)

    @staticmethod
    def reset() -> NoReturn:
        return os.execv(
            sys.executable, ['python'] + sys.argv
        )

    @staticmethod
    def exit() -> NoReturn:
        sys.exit()

    @staticmethod
    def console(name: str, color: str, message: str) -> None:
        print(MESSAGE.format(name, getattr(Colors, color.lower()), str(message)))

    @staticmethod
    def sleep(times: int) -> None:
        for i in range(times, 0, -1):
            for frame in FRAMES:
                sys.stdout.write(f'{frame}[{Colors.Orange}{i:02}{Colors.White}]')
                sys.stdout.flush()
                time.sleep(0.125)
        sys.stdout.write('\r')