import time



def spins(number) -> bool:
    delay = 0.002
    space = ' '*5
    
    crossbar = [
        f"\n{space}╔══════════╗",
        f"\n{space}╚══════════╝\n"
    ]
    try:
        print(crossbar[0])
        
        while delay < 0.1:
            number = (number % 98) + 1
            print(space + f"║ -> {number:02d} <- ║", end='\r')
            time.sleep(delay)
            delay += 0.001
        
        print(crossbar[-1])
        return True
    except KeyError:
        return False