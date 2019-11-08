import sys, os, math, string
import os.path as path
import random as r
import argparse
from distutils.errors import DistutilsFileError
from distutils.dir_util import copy_tree

from classes import *

#------------------------ Functions ------------------------
default_err_code = 2
ops = tuple(simple_func.simple_ops.keys())
uppercase_alphabets = r.sample(list(string.ascii_uppercase), k=len(ops))
all_functions = [simple_func(uppercase_alphabets[i], 'x', ops[i], r.randint(2, 9), bool(r.randint(0, 1))) for i in range(len(ops))]

#------------------------ Flags ----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description='function composition program. Default output is stdout. Network Connection is assumed but not required (see "--local")')
    parser.add_argument('-o', "--out", metavar='', type=argparse.FileType('w+', encoding='UTF-8'), help='Path to file for output, create file if necessary, not directories. Default output is stdout.')
    parser.add_argument('-f', '--num_functions', metavar='', type=int, default=3, help=f'number of functions to have as answer, must be at least 1, at most {len(ops)}. Default 3')
    parser.add_argument('-c', '--num_choices', metavar='', type=int, default=5, help='number of choices to present to the user, 1 < num choice <= factorial(num functions). Default 5')
    parser.add_argument('-q', '--num_questions', metavar='', type=int, default=1, help='number of questions to generate in file. Must be no greater than factorial(num functions). Default 1')
    parser.add_argument('-b', '--body_only', action='store_true', help='output only the form and submit without the html headers. Default False')
    parser.add_argument('-l', '--local', action='store_true', help='if flagged, will not fetch packages from CDN directly. Instead, required packages will be written in the same directory as file output within "packages/" directory(except for stdout). Default False.')
    parser.add_argument('-i', '--inverse', action='store_true', help='if flagged, will generate inverse questions, which lets user choose the function composition given an expression')
    return parser.parse_args(), parser

#------------------------ Main -----------------------------
def main():
    args, parser = parse_args()
    
    if args.num_functions < 1 or args.num_functions > len(ops) or \
    args.num_questions < 1 or args.num_questions > math.factorial(args.num_functions):
        help_and_exit(parser, default_err_code)
    if args.num_choices <= 1 or args.num_choices > math.factorial(args.num_functions):
        help_and_exit(parser, default_err_code)

    if args.out:
        fp = args.out
        # writing to file in local mode, need to put packages/ in same dir
        if args.local:
            proj_dir = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
            src = os.path.join(proj_dir, "assets/packages")
            dir_path, _ = os.path.split(os.path.realpath(fp.name))
            dest = os.path.join(dir_path, "packages")
            try:
                copy_tree(src, dest)
            except DistutilsFileError as e:
                sys.stderr.write(f"unexpected error occurred: {e}")
                sys.stderr.write('"--local" option unavailable')
                exit(default_err_code)
    else:
        fp = sys.stdout
    composer = function_composition(all_functions)
    writer = file_writer(fp, composer, args.num_functions, args.num_choices, args.num_questions, args.body_only, not args.local)
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
