from typing import Any, Callable, Literal
import ast
from .op_logic import OpLogic
from .node_interpreter import NodeInterpreter

class SafeEvaluator:
    @staticmethod
    def evaluate(expression,
                 **kwargs):
        _opLogic: OpLogic = OpLogic(mode=kwargs.get("mode", "none"))
        _inter: NodeInterpreter = NodeInterpreter()
        _inter._opLogic = _opLogic
        
        _inter.context_map(kwargs.get("context"))
        return _inter.eval_node(expression, )

if __name__ == "__main__":
    ...