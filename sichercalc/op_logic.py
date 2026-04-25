import ast
from typing import Any
from .exceptions import NodeEvaluationError
import operator

# Operator logic
def op_call(node_op,
            left,
            right):
    op_map = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow
    }
    try:
        l: Any = left
        r: Any = right
        return op_map[node_op](l, r)
    except KeyError:
        raise NodeEvaluationError(f"{repr(node_op)} operator not supported.")

if __name__ == "__main__":
    ...
