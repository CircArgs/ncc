import os
import re

# expected form of a C program, without line breaks
source_re = r"int main\s*\(\s*\)\s*{\s*return\s+(?P<ret>[0-9]+)\s*;\s*}" 

# Use 'main' instead of '_main' if not on OS X
assembly_format = """    
    .globl main
main:
    movl    ${}, %eax
    ret
"""
def lexer(args):
    with open(args.file, 'r') as infile, open(args.out, 'w') as outfile:
        source = infile.read().strip()
        match = re.match(source_re, source)

        # extract the named "ret" group, containing the return value
        retval = match.group('ret')
        outfile.write(assembly_format.format(retval))
