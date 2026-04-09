from typing import Any

class NodeError(Exception):
    ...

class ForbiddenNode(NodeError):
    ...

class BinaryOperationError(Exception):
    ...

class DivisionUndefinedError(BinaryOperationError):
    """
    x / 0
    """
    ...

class DivisionIndeterminateError(BinaryOperationError):
    """
    0 / 0
    """
    ...

if __name__ == "__main__":
    binop: tuple[int, Any, int] = (0, "ast.Div", 0)
    try:
        raise BinaryOperationError("")
    except BinaryOperationError:
        l: int = binop[0]
        op: Any = binop[1]
        r: int = binop[2]
        if op == "ast.Div":
            print(l, r)
            if l == 0 and r == 0:
                raise DivisionIndeterminateError("Zero divided by zero is indeterminated")
            elif l != 0 and r == 0:
                raise DivisionUndefinedError("A non-zero number divided by zero is undefined")
