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


# Function that connects input with the correct function
def operator(op, nums):
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
        nums.append(randint(10 ** (args.magn - 1), (10 ** args.magn) - 1))
    if args.single:
        nums[0 if args.op != 'd' else 1] = randint(1, 9)
    return nums


# Add function
def add(nums):
    return nums + [sum(nums)]

# Subtract function
def subtract(nums):
    return nums + [reduce(sub, nums)]

# Multiply function
def multiply(nums):
    return nums + [reduce(mul, nums)]

# Divide function
def divide(nums):
    return nums[:2] + [nums[0] / nums[1]]

# Square function
def square(nums):
    return [nums[0], nums[0] ** 2]

# Filter easy problems

# Write csv function
def write_to_csv(args):
    if os.path.exists(args.file):
        consent = input('File exists. Press y to overwrite.')
    if consent != 'y':
        exit()
    with open(args.file, 'w') as file:
        w = csv.writer(file)
        for _ in range(args.length):
            w.writerow(operator(args.op, generate_nums(args)))

# If __name__ == '__main__'
