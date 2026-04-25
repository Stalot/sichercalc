import ast
from typing import Any, Callable
from .op_logic import op_call
from .exceptions import NodeEvaluationError, OperationOverflowError, BinaryOperationError
from decimal import Decimal, InvalidOperation, Overflow, DecimalException

class NodeInterpreter:
    def __init__(self) -> None:
        self.instance_map = {
            str: self._string,
            ast.BinOp: self._binop,
            ast.UnaryOp: self._unaryop,
            ast.Constant: self._constant,
            ast.Expr: self._expr,
            ast.Module: self._module,
            ast.Call: self._call,
            ast.Name: self._name,
        }

        self.func_map: dict[str, Callable] = {}
        self.const_map: dict[str, Any] = {}

    def _convert(self, value: Any) -> Decimal:
       try:
           return Decimal(value) if not isinstance(value, str) else Decimal(value.strip())
       except (InvalidOperation, TypeError, ValueError):
           raise NodeEvaluationError(f"Cannot treat {type(value).__name__} ({value}) as a numeric value") 

    def _binop(self, node: ast.BinOp):
        left: Any = self.eval_node(node.left)
        left: Decimal = self._convert(left)
        op = node.op
        right: Any = self.eval_node(node.right)
        right: Decimal = self._convert(right)
        try:
            return op_call(type(op), left, right)
        except (OverflowError, Overflow):
            raise OperationOverflowError(f"Result of the arithmetic operation is too large to be represented",
                                         left,
                                         op,
                                         right)
        except (DecimalException, NodeEvaluationError) as nee:
            raise BinaryOperationError(str(nee),                                                   left,                                                       op,                                                         right)

    def _unaryop(self, node: ast.UnaryOp):
        if not isinstance(node.op, ast.USub):
            raise NodeEvaluationError(f"{type(node.op).__name__} operation is not supported")
        return -(self.eval_node(node.operand))

    def _string(self, node: str):
        return self.eval_node(ast.parse(node))

    def _constant(self, node: ast.Constant):
        value = node.value
        return self._convert(value)

    def _expr(self, node: ast.Expr):
        return self.eval_node(node.value)

    def _module(self, node: ast.Module):
        values = []
        for body in node.body:
            values.append(self.eval_node(body))
            if len(values) == 1:
                values = values[0]
        return values
    def _call(self, node: ast.Call):
        try:
            func_name = node.func.id
        except AttributeError:
            raise NodeEvaluationError(f"Can't call {type(node.func.value).__name__} object ({node.func.value}) as a function")
   
        try:
            args = [self.eval_node(arg) for arg in node.args]
            result = self.func_map[func_name](*args)
            return self._convert(result)
        except KeyError:
            raise NodeEvaluationError(f"Function '{func_name}' not supported")
    def _name(self, node: ast.Name):
        try:
            return self.const_map[node.id]
        except KeyError:
            raise NodeEvaluationError(f"Constant '{node.id}' not supported")

    def context_map(self, context) -> None:
        if not context:
            return None
        constants: None | dict[str, Any] = context.get("constants")
        functions: None | dict[str, Callable] = context.get("functions")
        if constants:
            for id, value in constants.items():
                try:
                    ast.literal_eval(str(value))
                    self.const_map.update({id: value})
                except ValueError as ve:
                    raise ValueError(f"All constants must be python literals, such as str, int, float, ... But got {ve}")
        if functions:
            for func_id, func in functions.items():
                if not isinstance(func, Callable):
                    raise ValueError(f"'{func}' is not callable")
                self.func_map[func_id] = func
    
    def clear_context_map(self) -> None:
        self.func_map = {}
        self.const_map = {}

    def eval_node(self, node: Any):
        _type: Any = type(node)
        if ast_instance := self.instance_map.get(_type):
            return ast_instance(node)
        raise NodeEvaluationError(f"{_type} is not supported")
        #except BinaryOperationError as boe:
        #    print(f"{boe.left=}")
        #    raise InvalidArithmeticError(f"{boe.binop_string} — {str(boe)}",
        #                                 boe.left,
        #                                 boe.op,
        #                                 boe.right)
if __name__ == "__main__":
    inter: NodeInterpreter = NodeInterpreter()
    new_logic = OpLogic("decimal")
    inter._opLogic=new_logic
    result = inter.eval_node("1.0383747*5.92838388229930")
    print(f"{result=}")
