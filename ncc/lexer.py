from collections import namedtuple
from enum import Enum

import parsy


class Keyword(Enum):
    Int = "int"
    Return = "return"
    If = "if"
    For = "for"


class Operator(Enum):
    Eq = "=="
    Lt = "<"
    Gt = ">"
    Lte = "<="
    Gte = ">="
    And = "&&"
    Or = "||"
    Plus = "+"
    Minus = "-"


class BitwiseOperator(Enum):
    Eq = "=="
    Xor = "^"
    Not = "~"
    And = "&"
    Or = "|"


class Parens(Enum):
    Left = "("
    Right = ")"


class Brackets(Enum):
    Left = "{"
    Right = "}"


Ident = namedtuple("Ident", "value")
Number = namedtuple("Number", "value")
Assign = namedtuple("Assign", [])
Semicolon = namedtuple("Semicolon", [])

space = parsy.regex(r"\s+")
padding = parsy.regex(r"\s*")
keyword = parsy.from_enum(Keyword) << space
paren = parsy.from_enum(Parens)
bracket = parsy.from_enum(Brackets)
semicolon = parsy.string(";").map(lambda _: Semicolon())
ident = parsy.regex(r"[a-zA-Z_][0-9a-zA-Z_]*").map(Ident)
number = parsy.regex(r"[0-9]+").map(int).map(Number)
assign = parsy.string("=").map(lambda _: Assign())
operator = parsy.from_enum(Operator)
binary_operator = parsy.from_enum(BitwiseOperator)

parser = keyword | ident | number | paren | bracket | semicolon | operator | binary_operator | assign


def lex(s):
    while s:
        token, rest = parser.parse_partial(s)
        if rest != s:
            s = rest.strip()
        else:
            raise ValueError(f"failed to parse stream '{rest}'")
        yield token


assembly_format = """
.globl main
main:
    movl    ${}, %eax
    ret
"""


def lexer(args):
    with open(args.file, "r") as infile, open(args.out, "w") as outfile:
        source = infile.read().strip()
        token_stream = lex(source)
        print(list(lex(source)))
        # extract the named "ret" group, containing the return value
        for token in token_stream:
            if token == Keyword.Return:
                break
        retval = next(token_stream)
        assert isinstance(retval, Number)
        outfile.write(assembly_format.format(retval.value))
