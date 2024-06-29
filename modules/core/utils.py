from modules.core.style import Colors



FRAMES: list[str] = [
    f"\r {Colors.white}[{Colors.yellow}{' ' * i}-->{' ' * (5 - i)}{Colors.white}]" 
    for i in range(6)
    ] + [
    f"\r {Colors.white}[{Colors.yellow}{' ' * i}<--{' ' * (5 - i)}{Colors.white}]" 
    for i in range(5, -1, -1)
]

MESSAGE: str = f"{Colors.white}[{Colors.green}{{}}{Colors.white}] --> {{}}{{}}{Colors.white}"