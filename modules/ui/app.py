import json

from modules.settings import UI
from modules.core.utils import Colors


def load_ui(
    colors: str, 
    banner_key: str, 
) -> None:
    with open(UI, 'r', encoding='utf-8') as file:
        banners = json.load(file)
    print(
        Colors.Diagonal(
            colors, 
            Colors.XCenter(Colors.Add("\n".join(banners[banner_key])))
        )
    )


def home() -> None:
    color = Colors.DynamicMIX([Colors.White, Colors.Purple])
    load_ui(color, 'home')


def menu() -> None:
    color = Colors.DynamicMIX([Colors.White, Colors.Orange])
    load_ui(color, 'menu')