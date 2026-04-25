from typing import Any
import decimal
import ast

class NodeEvaluationError(Exception):
    pass

class BinaryOperationError(NodeEvaluationError):
    def __init__(self,
                 msg: None | str,
                 left: Any,
                 op: ast.AST,
                 right: Any):
        self.msg: str = msg
        self.left: Any = left
        self.op: ast.AST = op
        self.right: Any = right
        node_map = {                                                    ast.Add: "+",                                               ast.Sub: "-",                                               ast.Div: "/",                                               ast.Mult: "*",                                              ast.Pow: "**",                                          }
        op_type = type(self.op)
        pretty_op: str = node_map.get(op_type, "?")
        self.binop_string: str = f"{self.left} {pretty_op} {self.right}"
        if not msg:
            self.msg = self.binop_string
        super().__init__(self.msg)

#class InvalidArithmeticError(BinaryOperationError, decimal.InvalidOperation, decimal.DivisionByZero):
#    pass

class OperationOverflowError(BinaryOperationError, decimal.Overflow):
    pass

if __name__ == "__main__":
    try:
        raise BinaryOperationError("Cannot divide by zero", 8, ast.Div, 0)
    except BinaryOperationError as boe:
        print(f"{boe.msg=}")
        print(f"{boe.binop_string=}")
