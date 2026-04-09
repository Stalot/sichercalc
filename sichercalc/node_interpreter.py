import ast
from typing import Any, Callable
from .op_logic import OpLogic
from .exceptions import ForbiddenNode, NodeError
from decimal import Decimal, InvalidOperation

class NodeInterpreter:
    _opLogic: OpLogic = OpLogic()

    def _convert(self,
                value: Any):
        value: str = str(value)
        try:
            value = Decimal(value)
        except InvalidOperation:
            raise NodeError(f"Couldn't convert {type(value).__name__} to a Decimal object")
        return value

    def _binop(self, node: ast.BinOp):
        left: Any = self.eval_node(node.left)
        left: float | Decimal = self._convert(left)
        op = node.op
        right: Any = self.eval_node(node.right)
        right: float | Decimal = self._convert(right)
        try:
            return self._opLogic.call(type(op), left, right)
        except KeyError:
            raise NodeError(f"{type(op).__name__} not supported")

    def _unaryop(self, node: ast.UnaryOp):
        if not isinstance(node.op, ast.USub):
            raise ForbiddenNode(f"{type(node.op).__name__} operation is not supported")
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
            raise NodeError(f"Can't call {type(node.func.value).__name__} object ({node.func.value}) as a function")
   
        try:
            args = [self.eval_node(arg) for arg in node.args]
            result = self.func_map[func_name](*args)
            return self._convert(result)
        except KeyError:
            raise NodeError(f"Function '{func_name}' not supported")
    def _name(self, node: ast.Name):
        try:
            return self.const_map[node.id]
        except KeyError:
            raise NodeError(f"Constant '{node.id}' not supported")
    
    instance_map = {
        str: _string,
        ast.BinOp: _binop,
        ast.UnaryOp: _unaryop,
        ast.Constant: _constant,
        ast.Expr: _expr,
        ast.Module: _module,
        ast.Call: _call,
        ast.Name: _name,
    }
    
    func_map: dict[str, Callable] = {}
    const_map: dict[str, int | float] = {}
    
    def set_op_logic(self, logic: OpLogic):
    	if not isinstance(logic, OpLogic):
    		raise TypeError(f"logic must be an OpLogic object, not {type(logic).__name__}!")
    	self._opLogic = logic

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
    
    def eval_node(self, node: Any):
        _type: Any = type(node)
        if ast_instance := self.instance_map.get(_type):
            return ast_instance(self, node)
        raise ForbiddenNode(f"{_type} is not supported")

if __name__ == "__main__":
    inter: NodeInterpreter = NodeInterpreter()
    new_logic = OpLogic("decimal")
    inter._opLogic=new_logic
    result = inter.eval_node("1.0383747*5.92838388229930")
    print(f"{result=}")
