import argparse
from pathlib import Path

from lexer import lexer

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=True)
parser.add_argument('--out', type=str)
args = parser.parse_args()
args.out=args.out or Path(args.file).parent/'a.s'
args.out=Path(args.out) if isinstance(args.out, str) else args.out
# print(args)
if __name__=="__main__":
    lexer(args)
