import doctest


def doctesting(a, b):
    '''
    Perform four arithmetic operations on two numbers and return the results.

    :param a: The first number.
    :param b: The second number.

    :return: A list containing the results of addition, subtraction, multiplication,
             and division of 'a' and 'b'.

    >>> doctesting(2, 3)
    [5, -1, 6, 0.6666666666666666]

    >>> doctesting(5, 10)
    [15, -5, 50, 0.5]
    '''
    results = []
    for operation in ["+", "-", "*", "/"]:
        solve = eval(str(a) + operation + str(b))
        results.append(solve)
    return results


if __name__ == '__main__':
    print(doctesting(2, 3))
    print(doctesting(5, 10))
    doctest.testmod(verbose=True)
    # or use python -m -v doctest Doctests.py
