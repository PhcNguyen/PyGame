import sys
import time
import os.path
import requests
import subprocess

from socket import socket
from typing import NoReturn
from modules.settings import VERSION
from modules.core.color import Colors
from modules.core.utils import FRAMES, MESSAGE


class System:
    Windows = os.name == 'nt'

    @staticmethod
    def Clear() -> int:
        """
        Clear() | Clears the terminal screen.
        """
        return os.system(
            "cls" if System.Windows else "clear"
        )
        
    @staticmethod
    def Command(command: str) -> int:
        """
        Command() | Executes a system command.
        """
        return os.system(command)

    @staticmethod
    def Reset() -> NoReturn:
        """
        Reset() | Resets the Python script by re-executing it.
        """
        return os.execv(
            sys.executable, ['python'] + sys.argv
        )

    @staticmethod
    def Exit() -> NoReturn:
        """
        Exit() | Exits the Python script.
        """
        sys.exit()

    @staticmethod
    def Console(name: str, color: str, message: str) -> None:
        """
        Console() | Prints a formatted message to the console.
        """
        print(MESSAGE.format(name, getattr(Colors, color), str(message)))

    @staticmethod
    def Sleep(times: int) -> None:
        """
        Sleep() | Shows a countdown with a specified number of frames.
        """
        for i in range(times, 0, -1):
            for frame in FRAMES:
                sys.stdout.write(f'{frame}[{Colors.Orange}{i:02}{Colors.White}]')
                sys.stdout.flush()
                time.sleep(0.125)
        sys.stdout.write('\r')    


def LoaclIP() -> str:
    try:
        with socket() as dns:
            dns.connect(("8.8.4.4", 80))
            return dns.getsockname()[0]
    except Exception as error:
        return error
        

def Github() -> None:
    start = time.time()
    System.Clear()

    try:
        response = requests.get('https://github.com')
        if response.status_code == 200:
            System.Console('Ping', 'Orange', 'Connect to "github.com" successful')
        else:
            System.Console('Ping', 'Red', f'Error: HTTP status code {response.status_code}')
            System.Exit()
    except Exception as e:
        System.Console('Ping', 'Red', str(e))
        System.Exit()

    try:
        commands = [
            (['git', 'add', '.'], 'git add .'),
            (['git', 'commit', '-m', VERSION], f'git commit -m "{VERSION}"'),
            (['git', 'push', 'origin', 'main'], 'git push origin main')
        ]
        
        for command, msg in commands:
            subprocess.run(command, stdout=-3, stderr=-3)
            System.Console('GitHub', 'Blue', msg)

        elapsed_time = time.time() - start
        System.Console('Timer', 'Yellow', f'Elapsed time for push: {elapsed_time:.2f} seconds')
    except FileNotFoundError:
        System.Console('GitHub', 'Red', 'Git command not found')
        System.Exit()
    except Exception as e:
        System.Console('GitHub', 'Red', f'Error executing Git command: {e}')
        System.Exit()