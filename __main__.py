import sys, os, math
import os.path as path
import argparse
import textwrap

from classes import *

#------------------------ Flags ----------------------------


#------------------------ Functions ------------------------


#------------------------ Main -----------------------------
def main():
    parser = argparse.ArgumentParser(description='Process function composition program')
    parser.add_argument('-o', "--outs", type=argparse.FileType('w+', encoding='UTF-8'), help='Path to file for output, create file if necessary. Default output is stdout.')
    parser.add_argument('-num_functions', type=int, default=3, help='number of functions to have as answer, must be at least 1. Default 3')
    parser.add_argument('-num_choices', type=int, default=5, help='number of choices to present to the user, 1 < num choice <= factorial(num functions). Default 5')
    parser.add_argument('-q', '--questions', type=int, default=1, help='number of questions to generate in file, default is 1. Must be no greater than factorial(num functions)')
    args = parser.parse_args()

    if args.num_functions < 1 or args.questions < 1:
        help_and_exit(parser)
    if args.num_choices <= 1 or args.num_choices > math.factorial(args.num_functions):
        help_and_exit(parser)

    if args.o:
        fp = args.o
    else:
        fp = sys.stdout
    # composer = function_composition(fn_list) # TODO: create a functions list
    # writer = file_writer(fp, composer, args.num_functions, args.num_choices, args.questions)
    # writer.dump()
    fp.close()
    exit(0)

def help_and_exit(parser, code=2):
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
