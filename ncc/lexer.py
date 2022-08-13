from dataclasses import dataclass
from enum import Enum
import re
import parsy


class Token:
    @classmethod
    def parser(cls, name):
        return parsy.string(getattr(cls, name).value)


class Keyword(Token, Enum):
    Return = "return "
    If = "if"
    For = "for"


class KeywordType(Token, Enum):
    Int = "int"


class Operator(Token, Enum):
    Eq = "=="
    Lt = "<"
    Gt = ">"
    Lte = "<="
    Gte = ">="
    And = "&&"
    Or = "||"
    Plus = "+"
    Minus = "-"


class BitwiseOperator(Token, Enum):
    Eq = "=="
    Xor = "^"
    Not = "~"
    And = "&"
    Or = "|"


class Parens(Token, Enum):
    Left = "("
    Right = ")"


class Brackets(Token, Enum):
    Left = "{"
    Right = "}"


@dataclass
class Ident(Token):
    value: str


@dataclass
class Number(Token):
    value: str


@dataclass
class Assign(Token):
    ...


@dataclass
class Semicolon(Token):
    ...


space = parsy.regex(r"\s+")
padding = parsy.regex(r"\s*")


class Tokens:
    keyword = parsy.from_enum(Keyword)
    keyword_type = parsy.from_enum(KeywordType)
    paren = parsy.from_enum(Parens)
    bracket = parsy.from_enum(Brackets)
    semicolon = parsy.string(";").result(Semicolon())
    ident = parsy.regex(r"[a-zA-Z_][0-9a-zA-Z_]*").desc("identifier").map(Ident)
    number = parsy.regex(r"[0-9]+").desc("number").map(Number)
    assign = parsy.string("=").result(Assign())
    operator = parsy.from_enum(Operator)
    binary_operator = parsy.from_enum(BitwiseOperator)

    parser = (
        keyword_type
        | keyword
        | ident
        | number
        | paren
        | bracket
        | semicolon
        | binary_operator
        | operator
        | assign
    )


def lex(s):
    while s:
        s = s.strip()
        try:
            token, rest = Tokens.parser.parse_partial(s)
            s = rest.strip()
        except:
            raise ValueError(f"failed to parse at '{rest}'")
        yield token


def lexer(args):
    with open(args.file, "r") as infile:
        infile = infile.read()
        infile = re.sub(r"\s+", " ", infile)
        return lex(infile)
