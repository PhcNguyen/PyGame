from pathlib import Path
import os.path


BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True

LANGUAGE = 'vi'

VERSION = open(
    os.path.join(BASE_DIR, 'modules', '.version')
).read().strip()

UI = os.path.join(BASE_DIR, 'modules', 'ui', 'ui.json')
