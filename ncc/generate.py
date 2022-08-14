"""code for AST->ASM"""
from functools import singledispatch

from ncc.parser import *


class State:
    _asm = """
    .globl main
    main:
        BODY
        ret
    """
    inserts=[]
    def insert(self, asm):
        # print(asm)
        self.inserts.append(asm)

    @property
    def asm(self):
        # print(self.inserts)
        return self._asm.replace('BODY', '\n'.join(self.inserts[::-1]))


def walk(ast, state: State):
    # print('AST ', ast)
    match ast:
        case Number(value):
            state.insert(f'movl ${value}, %eax')
        case Negate(value):
            state.insert('''//{n}
                    neg %eax''')
            walk(value, state)
        case LogicalNot(value):
            state.insert(f'''//{n} 
                cmpl $0, %eax
                movl $0, %eax
                sete %al
                    ''')
            walk(value, state)
        case BitwiseNot(value):
            state.insert(f'''//{n} 
                cmpl $0, %eax
                notl %eax
                    ''')
            walk(value, state)
        case Return(expr):
            walk(expr, state)
        case Function() as f:
            walk(f.return_, state)
        case Program(main):
            walk(main, state)


def generate(ast: Program, args):
    state=State()
    walk(ast, state)
    asm = state.asm
    # print(asm)
    with open(args.out, "w") as outfile:
        outfile.write(asm)
