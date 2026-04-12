from typing import Any
import decimal
import ast

class NodeEvaluationError(Exception):
    pass

class BinaryOperationError(NodeEvaluationError):
    def __init__(self,
                 msg: str,
                 left:  Any = None,
                 op: None | ast.AST = None,
                 right:  Any = None):
        self.left = left
        self.op = op
        self.right = right
        super().__init__(msg)

class DivisionByZeroError(BinaryOperationError, decimal.DivisionByZero):
        pass

class DivisionUndefinedError(DivisionByZeroError):
    """
    x / 0 (x != 0)
    """
    pass

class DivisionIndeterminateError(DivisionByZeroError, decimal.InvalidOperation):
    """
    0 / 0
    """
    pass

class OperationOverflowError(BinaryOperationError, decimal.Overflow):
    pass

if __name__ == "__main__":
    try:
        raise BinaryOperationError("cannot divide 8 by 0", 8, ast.Div, 0)
    except BinaryOperationError as binerr:
        print(f"{binerr.left=}")
        print(f"{binerr.op=}")
        print(f"{binerr.right=}")
