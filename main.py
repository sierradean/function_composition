import sys, os, math
import os.path as path
import argparse
import textwrap

from classes import *

parser = argparse.ArgumentParser(description='Process function composition program')
parser.add_argument('path', type=str, help='Absolute path to output html file')
parser.add_argument('name', type=str, help='file name to output content, create file if necessary (recommend .html)')
parser.add_argument('num_functions', type=int, help='number of functions to have as answer, must be at least 1')
parser.add_argument('num_choices', type=int, help='number of choices to present to the user, 1 < num choice <= factorial(num functions)')
parser.add_argument('-q', '--questions', type=int, default=1, help='number of questions to generate in file, default is 1. Must be no greater than factorial(num functions)')
args = parser.parse_args()

def main():
    if args.num_functions < 1 or args.questions < 1:
        help_and_exit()
    if args.num_choices <= 1 or args.num_choices > math.factorial(args.num_functions):
        help_and_exit()

    dir_path = args.path
    if not path.isabs(dir_path):
        help_and_exit()

    file_path = path.join(args.path, args.name)

    try:
        fp = open(file_path, 'w+')
    except OSError:
        fp = None
        print(f"Cannot output file to {file_path}")
        exit(1)
	
    composer = function_composition(fn_list) # TODO: create a functions list
    writer = file_writer(fp, composer, args.num_functions, args.num_choices, args.questions)
    writer.dump()
    fp.close()
    exit(0)

def help_and_exit(code=1):
    s = '''\
        ----------------------
        Invalid Input Occurred
        ----------------------
    '''
    print(textwrap.dedent(s))
    parser.print_help()
    exit(code)


if __name__ == '__main__':
	main()
