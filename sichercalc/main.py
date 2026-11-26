import ast
import operator
from decimal import Decimal, localcontext, InvalidOperation
from typing import Callable

class SafeEvaluator:
    def __init__(self):
        self.func_map: dict[str, Callable] = {}

    def set_function_whitelist(self, callables):
        self.func_map.clear()
        if isinstance(callables, (list, tuple, set)):
            for c in callables:
                self.func_map[str(c.__name__)] = c
        elif isinstance(callables, dict):
            self.func_map = callables
        else:
            raise TypeError(f"callables must be a list, tuple, set or dictionary, but got {type(callables).__name__}")

    def evaluate_expression(self, string: str) -> Decimal:
        if not isinstance(string, str):
            raise TypeError(f"string must be of type str, not {type(string).__name__}")
        return self._parse_string(string)

    # Parses the given string into a node tree, evaluates it node by node and then returns a Decimal object.
    def _parse_string(self, string: str) -> Decimal:
        node_tree = ast.parse(string)
        # The main ast node tree.
        # For example, if string is "2+2", node_tree will
        # look similar to:
        # Module(
        # | > body=Expr(
        # | >> value=BinOp(
        # | >>> left=Ast.Constant(id=2),
        # | >>> op=(Ast.Add, Ast.Sub, Ast.Mult, etc),
        # | >>> right=Ast.Constant(id=2),
        # | >> )
        # | > )
        # | )

        # inspect_node takes an ast node and, if in node_map, calls a dedicaded child method to evaluate that node — returns a Decimal value.
        def inspect_node(node) -> Decimal:
            def expr_node(): # ast.Expr
                return inspect_node(node.value)
            def binop_node(): # ast.BinOp
                # BinOp(left=(...), op=(...), right=(...))
                left = inspect_node(node.left) # The value of BinOp(...).left attribute after being evaluated by inspect_node()
                op = node.op # BinOp(...).op
                right = inspect_node(node.right) # Same with the left attribute, but now with BinOp(...).right

                # Map of allowed operators (+, -, *, /, and **)
                op_map = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                    ast.Pow: operator.pow,
                }
                if type(op) == ast.Pow:
                    if left > 10_000_000 or right > 10_000:
                        raise ValueError(f"{left} powered by {right} value is too big.")
                return op_map[type(op)](left, right)
            def name_node(): # ast.Name
                raise ValueError("variables not allowed")
            def constant_node(): # ast.Constant (positive numbers only)
                return Decimal(node.value)
            def unaryop_node(): # ast.UnaryOp (A unary operation, which is an operator that applied to only one value. (like negative numbers: -5, -2, -67, etc)
                op  = node.op
                operand = inspect_node(node.operand)
                if isinstance(op, ast.USub): # -x
                    return -operand
                elif isinstance(op, ast.UAdd): # +x
                    return operand
                else:
                    raise ValueError(f"{type(op).__name__} operation not supported")
            def module_node(): # ast.Module
                if not node.body:
                    raise ValueError("Input string is empty")
                return inspect_node(node.body)
            def call_node(): # ast.Call
                func_id = node.func.id
                args = [inspect_node(arg) for arg in node.args]
                kwargs = {kw.arg: inspect_node(kw.value) for kw in node.keywords}

                if func_id not in self.func_map:
                    raise ValueError(f"Function '{func_id}' not allowed.")
                try:
                    result: Decimal = self.func_map[func_id](*args, **kwargs)
                    if not isinstance(result, Decimal):
                        result = Decimal(str(result))
                    return result
                except (ValueError, TypeError, InvalidOperation, ZeroDivisionError) as e:
                    raise ValueError(f"An exception occurried during the execution of {func_id}: '{e}'")

            # Allowed nodes
            node_map = {
                ast.Expr: expr_node,
                ast.BinOp: binop_node,
                ast.Name: name_node,
                ast.Constant: constant_node,
                ast.Module: module_node,
                ast.UnaryOp: unaryop_node,
                ast.Call: call_node,
            }

            try:
                if type(node) == list:
                    node = node[0]
                return node_map[type(node)]()
            # Raises an exception if not in node_map
            except KeyError:
                raise ValueError(f"{type(node).__name__} object not allowed.")
        return inspect_node(node_tree)

if __name__ == "__main__":
    ...
