import sys, os, math, string
import os.path as path
import random as r
import argparse

from classes import *

#------------------------ Functions ------------------------
ops = tuple(simple_func.simple_ops.keys())
uppercase_alphabets = r.sample(list(string.ascii_uppercase), k=len(ops))
all_functions = [simple_func(uppercase_alphabets[i], 'x', ops[i], r.randint(2, 9)) for i in range(len(ops))]

#------------------------ Flags ----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description='Process function composition program. Default output is stdout.')
    parser.add_argument('-o', "--out", metavar='', type=argparse.FileType('w+', encoding='UTF-8'), help='Path to file for output, create file if necessary, not directories. Default output is stdout.')
    parser.add_argument('-f', '--num_functions', metavar='', type=int, default=3, help=f'number of functions to have as answer, must be at least 1, at most {len(ops)}. Default 3')
    parser.add_argument('-c', '--num_choices', metavar='', type=int, default=5, help='number of choices to present to the user, 1 < num choice <= factorial(num functions). Default 5')
    parser.add_argument('-q', '--num_questions', metavar='', type=int, default=1, help='number of questions to generate in file, default is 1. Must be no greater than factorial(num functions)')
    parser.add_argument('-b', '--body_only', action='store_true', help='output only the form and submit without the html headers')
    parser.add_argument('-w', '--web', action='store_true', help='integrate "src" link within html file output to fetch packages from CDN directly; this will require network connection! Default False.')
    return parser.parse_args(), parser

#------------------------ Main -----------------------------
def main():
    args, parser = parse_args()
    
    if args.num_functions < 1 or args.num_functions > len(ops) or \
    args.num_questions < 1 or args.num_questions > math.factorial(args.num_functions):
        help_and_exit(parser)
    if args.num_choices <= 1 or args.num_choices > math.factorial(args.num_functions):
        help_and_exit(parser)

    if args.out:
        fp = args.out
    else:
        fp = sys.stdout
    composer = function_composition(all_functions)
    writer = file_writer(fp, composer, args.num_functions, args.num_choices, args.num_questions, args.body_only, args.web)
    writer.dump()
    fp.close()
    exit(0)

def help_and_exit(parser, code=2):
    s = r'''
----------------------
Invalid Input Occurred
----------------------
    '''
    print(s)
    parser.print_help()
    exit(code)


if __name__ == '__main__':
    main()
