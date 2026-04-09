from typing import Any, Callable
from .op_logic import OpLogic
from .node_interpreter import NodeInterpreter
import ast

class AstEvaluator:
    _inter: NodeInterpreter = NodeInterpreter()
    _opLogic: OpLogic = OpLogic()

    def evaluate(self,
                 expression,
                 context: None | dict[str, dict[str, Any | Callable]] = None) -> str:
        self._inter: NodeInterpreter = NodeInterpreter()
        self._inter.set_op_logic(self._opLogic)
        self._inter.context_map(context)
        return str(self._inter.eval_node(expression))

    def set_operators(self, 
                      ops: dict[ast.AST, Callable],
                      update: bool = True) -> None:
        if not update:
            self._opLogic.set(op_map=ops)
            return
        self._opLogic.op_map.update(ops)

if __name__ == "__main__":
    ...
