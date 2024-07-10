def linear_search(arr, target):
    """
    Perform a linear search for the target in the array.

    Parameters:
    arr (list): The list to search through.
    target (any): The item to search for.

    Returns:
    int: The index of the target if found, otherwise -1.
    """
    for index, element in enumerate(arr):
        if element == target:
            return index
    return -1

# Example usage:
arr = [3, 5, 2, 4, 9]
target = 4
result = linear_search(arr, target)

if result != -1:
    print(f"Element found at index {result}")
else:
    print("Element not found in the array")
