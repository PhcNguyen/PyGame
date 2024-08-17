import socket



def localIP() -> str:
    # Create a dummy connection to determine the local IP without sending data
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
