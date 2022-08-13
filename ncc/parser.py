from dataclasses import dataclass
from typing import Iterable

from ncc.lexer import *

TokenStream = Iterable[Token]

@dataclass
class LogicalNot:
    value: Number

@dataclass
class BitwiseNot:
    value: Number

@dataclass
class Minus:
    value: Number

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
        case [n as Number]:
            return n
        case [Operator.Not, *rest]:
            return LogicalNot(parse(rest))
        case [Operator.Minus, *rest]:
            return Minus(parse(rest)) 
        case [BitwiseOperator.Not, *rest]:
            return BitwiseNot(parse(rest))       
        case [
            KeywordType.Int,
            Ident('main'),
            Parens.Left,
            Parens.Right,
            Brackets.Left,
            Keyword.Return,
            *rest,
            Semicolon,
            Brackets.Right,
        ]:
            main = Function(Ident('main'), KeywordType.Int, Return(parse(rest)))
            return Program(main)
        case _:
            raise Exception("Failed to Parse")
