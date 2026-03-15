import ast
import operator

ADD_OP = {
    ast.Add: operator.add
}
SUB_OP = {
    ast.Sub: operator.sub
}
MUL_OP = {
    ast.Mult: operator.mul
}
TRUEDIV_OP = {
    ast.Div: operator.truediv
}
FLOORDIV_OP = {
    ast.FloorDiv: operator.floordiv
}
MOD_OP = {
    ast.Mod: operator.mod
}
POW_OP = {
    ast.Pow: operator.pow
}
SHIFT_OP = {
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift
}
XOR_OP = {
    ast.BitXor: operator.xor
}
XOR_AS_POW_OP = {
    ast.BitXor: operator.pow
}

ARITHMETIC_BASIC = ADD_OP | SUB_OP | MUL_OP | TRUEDIV_OP | POW_OP
ARITHMETIC_FRIENDLY = ARITHMETIC_BASIC | XOR_AS_POW_OP
ARITHMETIC_EXTENDED = ARITHMETIC_BASIC | FLOORDIV_OP | MOD_OP
FULL_PYTHON_SYNTAX = ARITHMETIC_EXTENDED | SHIFT_OP | XOR_OP
DEFAULT_OP_MAP = ARITHMETIC_FRIENDLY