import ast
import operator
from typing import Any, Callable
from .exceptions import ForbiddenNode
from .finals import DEFAULT_OP_MAP

# Operators logic
class OpLogic():
    def __init__(self, precision_mode="float"):
        self.mode: str = ""
        self.set(precision_mode)

    op_map = DEFAULT_OP_MAP

    def set(self,
            precision_mode: None | str = None,
            op_map: None | dict[ast.AST, Callable] = None):
        if precision_mode:
            if not isinstance(precision_mode, str):
                raise TypeError(f"precision_mode must be a str, not {type(precision_mode).__name__}")
            self.mode = precision_mode
        if op_map:
            self.op_map = op_map
    def call(self,
             node_op,
             left,
             right):
        try:
            l: Any = left
            r: Any = right
            return self.op_map[node_op](l, r)
        except KeyError:
            raise ForbiddenNode(f"{node_op} operator not supported.")

if __name__ == "__main__":
    ...