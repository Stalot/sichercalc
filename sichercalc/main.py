from typing import Any, Callable
from .op_logic import OpLogic
from .node_interpreter import NodeInterpreter

class AstEvaluator:
    @staticmethod
    def evaluate(expression,
                 precision_mode: str = "float",
                 context: None | dict[str, dict[str, Any | Callable]] = None) -> str:
        _inter: NodeInterpreter = NodeInterpreter()
        _opLogic: OpLogic = OpLogic(precision_mode)
        _inter.set_op_logic(_opLogic)
        _inter.context_map(context)
        return str(_inter.eval_node(expression))

if __name__ == "__main__":
    ...