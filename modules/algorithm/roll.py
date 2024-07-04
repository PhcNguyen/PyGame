from random import randrange, sample, shuffle



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
    except Exception:
        return None


def rollDice() -> (tuple[int, list[str]] | None):
    '''
    Simulate rolling three dice.

    Returns:
    - tuple[int, list[str]]: Sum of the dice and a list of dice icons.
    '''
    dice_icon: dict[int, str] = {
        1: '⚀', 2: '⚁', 
        3: '⚂', 4: '⚃', 
        5: '⚄', 6: '⚅',
    }
    try:
        numbers: list[int] = sample(range(1, 7), 3)
        total = sum(numbers)
        icons = [dice_icon[n] for n in numbers]
        
        return total, icons
    except:
        return None