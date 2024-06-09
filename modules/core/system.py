import sys
import json
import time
import socket
import shutil
import os.path
import requests
import subprocess

from pathlib import Path
from typing import NoReturn
from modules.settings import VERSION
from modules.core.color import Colors
from modules.core.utils import FRAMES, MESSAGE


class Terminal:
    Windows = os.name == 'nt'

    @staticmethod
    def Clear() -> int:
        """
        Clear() | Clears the terminal screen.
        """
        return os.system(
            "cls" if Terminal.Windows else "clear"
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


class System:
    @staticmethod
    def remove_pycache() -> None:
        """
        remove pycache
        """
        for root, dirs, files in os.walk(Path.cwd()):
            for dir_name in dirs:
                if dir_name == "__pycache__":
                    pycache_dir = os.path.join(root, dir_name)
                    shutil.rmtree(pycache_dir)
            for file_name in files:
                if file_name.endswith(".pyc") or file_name.endswith(".pyo"):
                    pyc_file = os.path.join(root, file_name)
                    os.remove(pyc_file)

    @staticmethod
    def local_ip() -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dns:
                dns.connect(("8.8.4.4", 80))
                return dns.getsockname()[0]
        except Exception as error:
            raise error
        
    @staticmethod
    def load_language(language: str) -> dict:
        if language.lower() == 'vi':
            lang = 'Vietnamese'
        else:
            lang = 'English'
        try:
            with open('{}.json'.format(lang), 'r') as file:
                return json.load(file)
        except Exception as error:
            raise error


def Github() -> None:
    start = time.time()
    Terminal.Clear()

    try:
        response = requests.get('https://github.com')
        if response.status_code == 200:
            Terminal.Console('Ping', 'Orange', 'Connect to "github.com" successful')
        else:
            Terminal.Console('Ping', 'Red', f'Error: HTTP status code {response.status_code}')
            Terminal.Exit()
    except Exception as e:
        Terminal.Console('Ping', 'Red', str(e))
        Terminal.Exit()

    try:
        commands = [
            (['git', 'add', '.'], 'git add .'),
            (['git', 'commit', '-m', VERSION], f'git commit -m "{VERSION}"'),
            (['git', 'push', 'origin', 'main'], 'git push origin main')
        ]
        
        for command, msg in commands:
            subprocess.run(command, stdout=-3, stderr=-3)
            Terminal.Console('GitHub', 'Blue', msg)

        elapsed_time = time.time() - start
        Terminal.Console('Timer', 'Yellow', f'Elapsed time for push: {elapsed_time:.2f} seconds')
    except FileNotFoundError:
        Terminal.Console('GitHub', 'Red', 'Git command not found')
        Terminal.Exit()
    except Exception as e:
        Terminal.Console('GitHub', 'Red', f'Error executing Git command: {e}')
        Terminal.Exit()