from sichercalc import AstEvaluator
from sichercalc.exceptions import NodeError
import textwrap
from decimal import Overflow, InvalidOperation, DivisionByZero

evaluator = AstEvaluator()

def main():
    intro: str = textwrap.dedent("""\
    Welcome to SicherCalculator!
    Type 'q' to quit
    """)
    print(intro)
    while True:
        user_input = str(input("Expr: ")).strip()
        if user_input.lower() == "q":
            break
        try:
            result = evaluator.evaluate(user_input,
                                        "decimal")
            print(result)
        except (NodeError, SyntaxError):
            print(f"Err: Invalid input.")
        except Overflow:
            print("Err: I can't count to that, sorry.")
        except DivisionByZero:
            print("Err: Cannot divide by zero.")
        except InvalidOperation:
            print("Err: Invalid decimal operation.")

if __name__ == "__main__":
    main()