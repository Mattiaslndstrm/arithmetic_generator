from random import randint
import os
import argparse
import csv


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

# Filter easy problems

# Add function

# Subtract function

# Multiply function

# Divide function

# Square function

# Function that connects input with the correct function

# Write csv function

# If __name__ == '__main__'
