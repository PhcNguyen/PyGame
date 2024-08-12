import time
from random import randrange, shuffle, randint



def listNumber(
    ratio: float = 0.7
) -> (list[int] | bool):
    '''
    Generate a list of numbers with a specified ratio of odd to even numbers.
    
    Parameters:
    - ratio (float): The ratio of odd to even numbers (0.1 to 1.0).

    Returns:
    - list[int]: List containing odd and even numbers based on the ratio.
    - bool: If the ratio is invalid.
    '''
    if not 0 < ratio < 1:
        return False
    
    odd_count: int = int(100 * ratio)
    even_count: int = 100 - odd_count

    try:    
        odd: list[int] = [
            randrange(1, 99, 2) for _ in range(odd_count)
        ]
        even: list[int] = [
            randrange(2, 99, 2) for _ in range(even_count)
        ]
        numbers: list[int] = odd + even; shuffle(numbers)

        return numbers
    except KeyError:
        return False


def rollDice(
) -> (tuple[int, list[str]] | bool):
    '''
    Simulate rolling three dice.

    Returns:
    - tuple[int, list[str]]: Sum of the dice and a list of dice icons.
    - bool: If an error occurs.
    '''
    dice_icon: dict[int, str] = {
        1: '⚀', 2: '⚁', 3: '⚂', 
        4: '⚃', 5: '⚄', 6: '⚅',
    }
    try:
        numbers: list[int] = [randint(1, 6) for _ in range(3)]
        total: int = sum(numbers)
        icons: list[str] = [dice_icon[n] for n in numbers]
        
        return total, icons
    except KeyError:
        return False


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


def checkDice(select, numbers) -> int:
    # Dictionary containing conditions for different selections
    conditions: dict[int, list[int]] = {
        1: [11, 12, 13, 14, 15, 16, 17],  # Tai (big)
        2: [4, 5, 6, 7, 8, 9, 10],        # Xiu (small)
        3: [4, 6, 8, 10, 12, 14, 16, 18], # Chan (even)
        4: [3, 5, 7, 9, 11, 13, 15, 17]   # Le (odd)
    }

    # Check if the selected category exists in the conditions dictionary
    if select in conditions:
        # Return 1 if the number is in the selected condition list, otherwise return 0
        return int(numbers in conditions[select])
    # Return 0 if the selected category does not exist in the conditions dictionary
    return 0