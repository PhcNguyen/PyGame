from random import randrange, sample



def listNumber(
    ratio: float = 0.7
) -> (list[int] | None):
    '''
    0.1 -> 0.9
    0.7: "70 odd - 30 even"
    0.8: "80 odd - 20 even"
    '''
    try:
        odd_count: int = int(100 * ratio)
        even_count: int = 100 - odd_count
            
        odd: list[int] = [
            randrange(1, 99, 2) for _ in range(odd_count)
        ]
        even: list[int] = [
            randrange(2, 99, 2) for _ in range(even_count)
        ]
        
        return odd + even
    except Exception:
        return None


def rollDice() -> tuple[int, list[str]]:
    dice_icon = {
        1: '⚀', 2: '⚁', 3: '⚂',
        4: '⚃', 5: '⚄', 6: '⚅',
    }
    number = sample(range(1, 7), 3)
    return sum(number), [dice_icon[i] for i in number]
