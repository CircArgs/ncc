import argparse
import os

from ncc.lexer import lexer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    parser.add_argument("-o", "--out", type=str)
    parser.add_argument("-c", "--clean", action="store_true")
    args = parser.parse_args()
    args.out = args.out or ".".join(args.file.split(".")[:-1])
    args.out += ".s"
    lexer(args)
    os.system(f"gcc -m32 {args.out} -o {'.'.join(args.out.split('.')[:-1])}")
    if args.clean:
        os.remove(args.out)


if __name__ == "__main__":
    main()
