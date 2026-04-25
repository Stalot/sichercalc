from typing import Any
from .node_interpreter import NodeInterpreter
import ast

class AstEvaluator:
    def __init__(self):
        self._inter: NodeInterpreter = NodeInterpreter()

    def evaluate(self,
                 expression,
                 context: None | dict[str, dict[str, Any]] = None) -> str:
        # Clears the previous context
        self._inter.clear_context_map()

        if context:
            # Local context:
            self._inter.context_map(context)
        return str(self._inter.eval_node(expression))

if __name__ == "__main__":
    ...
