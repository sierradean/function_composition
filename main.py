import sys, os, math
import os.path as path
import argparse

parser = argparse.ArgumentParser(description='Process function composition program')
parser.add_argument('path', type=str, help='Absolute path to output html file')
parser.add_argument('name', type=str, help='file name to output content, create file if necessary')
parser.add_argument('num_functions', type=int, help='number of functions to have as answer')
parser.add_argument('num_choices', type=int, help='number of choices to present to the user')
args = parser.parse_args()

def main():
    if args.num_functions < 1:
        print('Invalid number of functions')
        exit(1)
    if args.num_choices < 1 or args.num_choices > math.factorial(args.num_functions):
        print('Invalid number of choices')
        exit(1)

    dir_path = args.path
    if not path.isabs(dir_path):
        print('Invalid path. Path must be absolute path')
        exit(1)

    file_path = path.join(args.path, args.name)

    try:
        fp = open(file_path, 'w+')
    except OSError:
        fp = None
        print(f"Cannot output file to {file_path}")
        exit(1)
	
	# look into eval() that seems to parse functions for us
	# fp.close()


if __name__ == '__main__':
	main()