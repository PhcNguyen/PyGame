import random



def ratioNumber(ratio: float = 0.7) -> int:
    '''
    Generate a list of 100 numbers with a specified ratio of odd to even numbers
    and return one random number from the list. Returns -1 if the ratio is invalid.
    
    Parameters:
    - ratio (float): The ratio of odd to even numbers (0.0 to 1.0).
    
    Returns:
    - int: A single number from the generated list based on the ratio.
           Returns -1 if the ratio is invalid.
    '''
    if not 0.0 <= ratio <= 1.0:
        return -1  # Use -1 to indicate invalid ratio

    # Generate list of numbers with the desired ratio of odd to even
    numbers = [
        random.randrange(1, 100, 2) if i < int(100 * ratio)
        else random.randrange(2, 100, 2)
        for i in range(100)
    ]
    
    # Shuffle the list to ensure randomness
    random.shuffle(numbers)
    
    # Return a single number from the list
    return random.choice(numbers)



def rollDice() -> (tuple[int, list[str]] | bool):
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
    
    numbers: list[int] = [random.randint(1, 6) for _ in range(3)]
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