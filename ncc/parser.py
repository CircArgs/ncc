from dataclasses import dataclass
from typing import Iterable

from ncc.lexer import *

TokenStream = Iterable[Token]


@dataclass
class Return:
    value: Number


@dataclass
class Function:
    name: Ident
    return_type: KeywordType
    # body: Return
    return_: Return | None = None


@dataclass
class Program:
    main: Function


def parse(tokens: TokenStream):
    tokens = list(tokens)
    # print("*" * 25, "\n", tokens, "\n", "*" * 25)
    match tokens:
        case [
            KeywordType.Int,
            main as Ident,
            Parens.Left,
            Parens.Right,
            Brackets.Left,
            Keyword.Return,
            n as Number,
            Semicolon,
            Brackets.Right,
        ]:
            main = Function(main, KeywordType.Int, Return(n))
            return Program(main)
        case _:
            raise Exception("Failed to Parse")
