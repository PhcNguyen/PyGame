from random import randrange, shuffle, randint



def listNumber(
    ratio: float = 0.7
) -> (list[int] | None):
    '''
    Generate a list of numbers with a specified ratio of odd to even numbers.
    
    Parameters:
    - ratio (float): The ratio of odd to even numbers (0.1 to 1.0).

    Returns:
    - list[int]: List containing odd and even numbers based on the ratio.
    - None: If the ratio is invalid.
    '''
    if not 0 < ratio < 1:
        return None
    
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
        return None


def rollDice() -> (tuple[int, list[str]] | None):
    '''
    Simulate rolling three dice.

    Returns:
    - tuple[int, list[str]]: Sum of the dice and a list of dice icons.
    - None: If an error occurs.
    '''
    dice_icon: dict[int, str] = {
        1: '⚀', 2: '⚁', 
        3: '⚂', 4: '⚃', 
        5: '⚄', 6: '⚅',
    }
    try:
        numbers: list[int] = [randint(1, 6) for _ in range(3)]
        total: int = sum(numbers)
        icons: list[str] = [dice_icon[n] for n in numbers]
        
        return total, icons
    except KeyError:
        return None