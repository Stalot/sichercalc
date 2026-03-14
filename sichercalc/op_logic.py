import ast
import operator 
from decimal import Decimal, InvalidOperation

# Operators logic
class OpLogic():
    def __init__(self, precision_mode="float"):
        if not isinstance(precision_mode, str):
          raise TypeError(f"precision_mode must be a str, not {type(precision_mode).__name__}")
        self.mode: str = precision_mode
    op_map = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitAnd: operator.and_,
        ast.BitXor: operator.xor,
    }

    def call(self,
             node_op,
             left,
             right):
        def convert(number: int | float) -> int | float | Decimal:
            new_number = number
            match self.mode:
                case "float":
                    new_number = float(number)
                case "decimal": 
                    try:
                        new_number = Decimal(str(number))
                    except InvalidOperation:
                        raise ValueError(f"Couldn't convert {type(number).__name__} '{number}' to a Decimal object")
                case _:
                    raise ValueError(f"'{self.mode}' precision mode is unknown. Valid modes are: float and decimal")
            return new_number
        try:
            l: int | float | Decimal = convert(left)
            r: int | float | Decimal = convert(right)
            return self.op_map[node_op](l, r)
        except KeyError:
            raise ValueError(f"{node_op} operator not supported.")

if __name__ == "__main__":
    opLogic = OpLogic("0")
    result = opLogic.call(ast.Mult, 2.722772727, 3.1483828293388383)
    print(result)