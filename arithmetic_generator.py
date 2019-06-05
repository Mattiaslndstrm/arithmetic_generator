from random import randint
import os
import argparse
import csv
from functools import reduce
from operator import sub, mul


def get_command_line_input():
    """Return an argparse.Namespace from command line arguments."""
    parser = argparse.ArgumentParser(
         description=('Generates csv-files with arithmetic problems for '
                      'easy import into Anki or other SRS-software.'))
    parser.add_argument('file', help='filename for the csv-file')
    parser.add_argument('op', choices=('a', 's', 'm', 'd', 'sq'),
                        help='arithmetic operation (add/subtract/multiply/'
                             'divide/square)')
    parser.add_argument('length', type=int, help='number of problems')
    parser.add_argument('magn', type=int,
                        help='order of magnitude (number of digits, 3 = 100-999)')
    parser.add_argument('terms', type=int, help='number of terms')
    parser.add_argument('--single', default=False, action='store_true',
                        help=('converts the first term to a single digit (for'
                              ' division the second term)'))
    return parser.parse_args()


def operator(op, nums):
    """Returns the result of op(nums) where op corresponds to a funciton

    Input:
    op (str): specifies operator (a, s, m, d, sq)
    nums (list): a list of numbers that the function corresponding to op will
                 be applied to

    Output:
    list: The result of the function call op(nums)
    """
    return {
        'a': add,
        's': subtract,
        'm': multiply,
        'd': divide,
        'sq': square,
    }.get(op, 'add')(nums)


def generate_nums(args):
    """Returns a list of terms where size and number is specifed in args

    Input:
    args (argparse.Namespace): Command line arguments

    Output:
    nums (list): a list of terms to be calculated where the size of the numbers
                 is specified in args.magn and the number of numbers specified
                 in args.terms.
    """
    nums = []
    for _ in range(args.terms):
        while True:
            n = randint(10 ** (args.magn - 1), (10 ** args.magn) - 1)
            if validate(n, args):
                nums.append(n)
                break
    if args.single:
        nums[0 if args.op != 'd' else 1] = randint(1, 9)
    return nums


def validate(n, args):
    """Returns True if n is not divisible by 10 or 5 or too close depending
    on size of n else False

    Input:
    n (int): The number to be tested.
    args (argparse.Namespace): Command line arguments

    Output:
    bool: True if n is between 11 and 99 and not divisible by 10
          or 1000 and bigger and not divisible by 5 or +/- 15 of any number
          divisible with 100
          or single digit
          else False
    """
    if args.magn == 2:
        return n % 10 != 0
    elif args.magn >= 3:
        return n % 100 > 15 and n % 100 < 85 and n % 5 != 0
    return True


def add(nums):
    """Returns the list nums with the sum of the digits appended.

    Input:
    nums (list): a list of numbers

    Output
    list: the list nums with the sum of nums appended as the last
                   element in the list
    """
    return nums + [sum(nums)]


def subtract(nums):
    """Returns the list nums with the difference of the digits appended and the
    first number changed to an order of magnitude larger

    Input:
    nums (list): a list of numbers

    Output
    list:: the list nums with the sum of nums appended as the last
                   element in the list and the first number changed to a new
                   random number one order of magnitude larger than the
                   previous number.
    """
    nums[0] = randint(10 ** len(str(nums[0])), 10 ** (len(str(nums[0])) + 1)-1)
    return nums + [reduce(sub, nums)]


def multiply(nums):
    """Returns the list nums with the product of the digits appended.

    Input:
    nums (list): a list of numbers

    Output
    list:: the list nums with the product of nums appended as the last
                   element in the list
    """
    return nums + [reduce(mul, nums)]


def divide(nums):
    """Returns the first and second element of nums with the quotient of those
    appended. The second element is changed to number between 2 and

    Input:
    nums (list): a list of numbers

    Output
    list:: The first element, the second element and their quotient
                   The second element is changed to number between 11 and 99 if
                   larger.
    """
    nums[1] = randint(2 if nums[1] < 10 else 11, 9 if nums[1] < 10 else 99)
    return nums[:2] + [nums[0] / nums[1]]


def square(nums):
    """Returns the first element in nums and its square.

    Input:
    nums (list): a list of numbers

    Output:
    list: the first number of nums and its square.
    """
    return [nums[0], nums[0] ** 2]


def write_to_csv(args):
    """Writes the number of problems to the file specified in args if the file
    doesn't exists or the user gives consent to overwrite.

    Input:
    args (argparse.Namespace): Command line arguments

    Sideeffect:
    exits the program if file exists and user doesn't input 'y'. Else writes
    the number of problems to args.file.
    """
    if os.path.exists(args.file):
        consent = input('File exists. Press y to overwrite.')
        if consent != 'y':
            exit()
    with open(args.file, 'w') as file:
        w = csv.writer(file, delimiter=';')
        for _ in range(args.length):
            w.writerow(operator(args.op, generate_nums(args)))


if __name__ == '__main__':
    write_to_csv(get_command_line_input())
