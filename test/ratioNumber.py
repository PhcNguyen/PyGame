from services.algorithm import ratioNumber


def test_numberByRatio():
    # Test case 1: Valid ratio (0.0)
    result = ratioNumber(0.0)
    assert result % 2 == 0, f"Expected even number but got {result}"

    # Test case 2: Valid ratio (1.0)
    result = ratioNumber(1.0)
    assert result % 2 != 0, f"Expected odd number but got {result}"

    # Test case 3: Valid ratio (0.5)
    results = [ratioNumber(0.5) for _ in range(100)]
    odd_count = sum(1 for r in results if r % 2 != 0)
    even_count = 100 - odd_count
    assert abs(odd_count - even_count) < 20, f"Odd and even numbers should be roughly balanced but got {odd_count} odd and {even_count} even numbers"

    # Test case 4: Invalid ratio (below 0.0)
    result = ratioNumber(-0.1)
    assert result == -1, f"Expected -1 for invalid ratio but got {result}"

    # Test case 5: Invalid ratio (above 1.0)
    result = ratioNumber(1.1)
    assert result == -1, f"Expected -1 for invalid ratio but got {result}"

    print("All test cases passed.")

# Run the tests
test_numberByRatio()