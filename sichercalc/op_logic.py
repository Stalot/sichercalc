import ast
from typing import Any, Callable
from .exceptions import NodeEvaluationError
from .finals import DEFAULT_OP_MAP

# Operators logic
class OpLogic():
    def __init__(self) -> None:
        self.op_map = DEFAULT_OP_MAP

    def call(self,
             node_op,
             left,
             right):
        try:
            l: Any = left
            r: Any = right
            return self.op_map[node_op](l, r)
        except KeyError:
            raise NodeEvaluationError(f"{repr(node_op)} operator not supported.")

if __name__ == "__main__":
    ...
