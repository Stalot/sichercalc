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

class DivisionIndeterminatedError(BinaryOperationError):
    """
    0 / 0
    """
    ...

class OperationOverFlowError(BinaryOperationError):
    ...

if __name__ == "__main__":
    ...
