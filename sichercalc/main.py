from typing import Any
from .node_interpreter import NodeInterpreter
import ast
from decimal import Decimal, localcontext, ROUND_HALF_UP

class AstEvaluator:
    def __init__(self):
        self._inter: NodeInterpreter = NodeInterpreter()

    def evaluate(self,
                 expression: str,
                 context: None | dict[str, dict[str, Any]] = None,
                 quantize: None | str = "0.000001",
                 rounding: None | str = ROUND_HALF_UP,
                 normalize: bool = True,) -> str:
        # Clears the previous context
        self._inter.clear_context_map()

        if context:
            self._inter.context_map(context)
        evaluated_result: Decimal = self._inter.eval_node(expression)

        # Quantizes the result after evaluation, it doesn't apply to internal calculation.
        if quantize:
            if not isinstance(quantize, str):
                raise TypeError(f"quantize must be a string, not {type(quantize)!r}")
            evaluated_result = evaluated_result.quantize(Decimal(quantize),
                                                         rounding=rounding)
        # Normalizes the result after evaluation, it doesn't apply to internal calculation.
        if normalize:
            if not isinstance(normalize, bool):
                raise TypeError(f"normalize must be a boolean, not {type(normalize)!r}")
            evaluated_result = evaluated_result.normalize()
        return str(evaluated_result)

    def trunc(self,
              x: Any,
              places: int) -> str:
        """
        Truncates a number to a specific number of decimal places.
        """
        number: str = str(x)
        decimal_places: int = int(places)
        period: int = number.find(".") # returns -1 if not found
        if period != -1:
            trunc: str = number[period:period+1+decimal_places]
            number: str = number[:period] + trunc
            # removes trailing zeros
            if trunc.endswith("0"):
                number = str(Decimal(number).normalize())
        return number


if __name__ == "__main__":
    ...
