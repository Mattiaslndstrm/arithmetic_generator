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
    if args.magn == 2:
        return n % 10 != 0
    elif args.magn >= 3:
        return n % 100 > 15 and n % 100 < 85 and n % 5 != 0
    return True


def add(nums):
    return nums + [sum(nums)]


def subtract(nums):
    nums[0] = randint(10 ** len(str(nums[0])), 10 ** (len(str(nums[0])) + 1)-1)
    return nums + [reduce(sub, nums)]


def multiply(nums):
    return nums + [reduce(mul, nums)]


def divide(nums):
    nums[1] = randint(2 if nums[1] < 10 else 11, 9 if nums[1] < 10 else 99)
    return nums[:2] + [nums[0] / nums[1]]


def square(nums):
    return [nums[0], nums[0] ** 2]


def write_to_csv(args):
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
