from typing import Any, Callable, Literal
import ast
from .op_logic import OpLogic

class SafeEvaluator:
    @classmethod
    def evaluate(cls,
                 expression,
                 context: None | dict[str, Any] = None,
                 **kwargs):
        _opLogic = OpLogic(mode=kwargs.get("mode", "float"))
        func_map: dict[str, Callable] = {}
        const_map: dict[str, int | float] = {}
        
        def context_map(context) -> None:
            if not context:
                return None
            constants: None | dict[str, Literal] = context.get("const")
            functions: None | dict[str, Callable] = context.get("func")
            if constants:
                for id, value in constants.items():
                    try:
                        ast.literal_eval(str(value))
                        const_map.update({id: value})
                    except ValueError as ve:
                        raise ValueError(f"All constants must be python literals, such as str, int, float, ... But got {ve}")
            if functions:
                for id, func in functions.items():
                    if not isinstance(func, Callable):
                        raise ValueError(f"'{func}' is not callable")
                    func_map.update({id: func})
        def node_evaluation(node):
            if isinstance(node, (list, tuple)):
                return [node_evaluation(sub_node) for sub_node in node]

            elif isinstance(node, str):
                return node_evaluation(ast.parse(node))

            elif isinstance(node, ast.Module):
                values = []
                for body in node.body:
                    values.append(node_evaluation(body))
                if len(values) == 1:
                    values = values[0]
                return values

            elif isinstance(node, ast.Expr):
                return node_evaluation(node.value)

            elif isinstance(node, ast.BinOp):
                left = node_evaluation(node.left)
                op = node.op
                right = node_evaluation(node.right)

                try:
                    #return cls.op_map[type(op)](left, right)
                    return _opLogic.call(type(op), left, right)
                except KeyError:
                    raise ValueError(
                        "Operator %s not supported" % op.__class__.__name__)

            elif isinstance(node, ast.Call):
                try:
                    func_name = node.func.id
                except AttributeError:
                    raise ValueError(f"{node.func.value}: Can't call {type(node.func.value).__name__} object as a function")
                args = [node_evaluation(arg) for arg in node.args]

                try:
                    return func_map[func_name](*args)
                except KeyError:
                    raise ValueError("Function %s not supported" % func_name)

            elif isinstance(node, ast.Constant):
                return node.value

            elif isinstance(node, ast.Name):
                try:
                    return const_map[node.id]
                except KeyError:
                    raise ValueError("Constant %s not supported" % node.id)

            raise TypeError("Unsupported operation: %s" % node.__class__.__name__)
        context_map(context)
             
        return node_evaluation(expression)

if __name__ == "__main__":
    se = SafeEvaluator()
    constants = {"aaa": "2653.0000000000000000000000000000000"}
    def zero():
        return 0
    functions = {"zero": zero}
    context = {
        "const": constants,
        "func": functions
    }
    def my_func():
        ...
    result = se.evaluate("2+2/1", context)
    print(result)