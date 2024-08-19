from random import randrange, shuffle, randint, choice



def listNumber(
    ratio: float = 0.7
) -> list[int] | bool:
    '''
    Generate a list of numbers with a specified ratio of odd to even numbers.
    
    Parameters:
    - ratio (float): The ratio of odd to even numbers (0.1 to 1.0).

    Returns:
    - list[int]: List containing odd and even numbers based on the ratio.
    - bool: If the ratio is invalid.
    '''
    if not 0.0 <= ratio <= 1.0:
        return False
    
    numbers: list[int] = [
        randrange(1, 99, 2) if i < int(100 * ratio) 
        else randrange(2, 99, 2) 
        for i in range(100)
    ]
    shuffle(numbers)
    numbers = choice(numbers)
    return numbers


def rollDice() -> tuple[int, list[str]] | bool:
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
    
    numbers: list[int] = [randint(1, 6) for _ in range(3)]
    total: int = sum(numbers)
    icons: list[str] = [dice_icon[n] for n in numbers]
    
    return total, icons


def checkDice(select: int, numbers: int) -> int:
    '''
    Check the result of the dice roll against the selected condition.

    Parameters:
    - select (int): Selected condition (1-4).
    - numbers (int): Sum of the dice roll.

    Returns:
    - int: 1 if the condition is met, 0 otherwise.
    '''
    conditions: dict[int, list[int]] = {
        1: [11, 12, 13, 14, 15, 16, 17],  # Tai (big)
        2: [4, 5, 6, 7, 8, 9, 10],        # Xiu (small)
        3: [4, 6, 8, 10, 12, 14, 16, 18], # Chan (even)
        4: [3, 5, 7, 9, 11, 13, 15, 17]   # Le (odd)
    }

    return int(numbers in conditions.get(select, []))
