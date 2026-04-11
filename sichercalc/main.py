from typing import Any, Callable
from .op_logic import OpLogic
from .node_interpreter import NodeInterpreter
import ast

class AstEvaluator:
    _inter: NodeInterpreter = NodeInterpreter()
    _opLogic: OpLogic = OpLogic()
    _global_context: dict[str, dict[str, Any]] = {}

    def evaluate(self,
                 expression,
                 context: None | dict[str, dict[str, Any]] = None) -> str:
        # Clears the current context
        self._inter.clear_context_map()

        self._inter: NodeInterpreter = NodeInterpreter()
        self._inter.set_op_logic(self._opLogic)
        if context:
            # Local context:
            # Global context will be ignored if a local
            # context is defined
            self._inter.context_map(context)
        else:
            # Global context:
            # Will be applied to every evaluate() call
            # that doesn't have a local context defined
            self._inter.context_map(self._global_context)
        return str(self._inter.eval_node(expression))

    def set_operators(self, 
                      ops: dict[ast.AST, Callable],
                      update: bool = True) -> None:
        if not update:
            self._opLogic.set(op_map=ops)
            return
        self._opLogic.op_map.update(ops)

    def set_global_context(self,
                           global_context: dict[str, dict[str, Any]]):
        self._global_context = global_context

if __name__ == "__main__":
    ...
