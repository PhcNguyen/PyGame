import os
import time
import pathlib
import requests
import subprocess

from modules.core.system import System



class Github:
    start = time.time()
    version = pathlib.Path(__file__).parent.joinpath('version').read_text().strip()

    @staticmethod
    def connect(url: str | bytes) -> bool:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                System.console('Ping', 'Orange', f'Connect to "{url.split('//')[-1]}" successful')
                return True
            else:
                System.console('Ping', 'Red', f'Error: HTTP status code {response.status_code}')
                return False
        except Exception as e:
            System.console('Ping', 'Red', str(e))
            return False

    @staticmethod
    def command(command, message) -> None:
        try:
            subprocess.run(command, -1, None, None, -3, -3)
            System.console('GitHub', 'Blue', message)
        except FileNotFoundError:
            System.console('GitHub', 'Red', 'Git command not found')
            System.exit()
        except Exception as e:
            System.console('GitHub', 'Red', f'Error executing Git command: {e}')
            System.exit()

    @staticmethod
    def automatic() -> None:
        if not Github.connect('https://github.com'):
            System.exit()
        
        commands = [
                (['git', 'add', '.'], 'git add .'),
                (['git', 'commit', '-m', Github.version], f'git commit -m "{Github.version}"'),
                (['git', 'push', 'origin', 'main'], 'git push origin main')
        ]
        for command in commands:
            Github.command(command[0], command[-1])
        
        System.console(
            'Timer', 'Yellow', 
            f'Elapsed time for push: {(time.time() - Github.start):.2f} seconds'
        )