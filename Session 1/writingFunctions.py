"""
Will Dudley's file
Created on 16/01/2024
"""


def squareList(arr: list) -> list:
    """
    :param arr: Input array to be squared
    :return: A list containing the square of each element of the input list
    """
    return [x ** 2 for x in arr]


print(squareList([1, 2, 3]))
