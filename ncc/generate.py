"""code for AST->ASM"""

from ncc.lexer import *
from ncc.parser import *


def generate(ast: Program, args):
    assembly_format = """
    .globl main
    main:
        movl    ${}, %eax
        ret
    """
    with open(args.out, "w") as outfile:
        retval = ast.main.return_.value
        assert isinstance(retval, Number)
        outfile.write(assembly_format.format(retval.value))
