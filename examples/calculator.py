from sichercalc import AstEvaluator
from sichercalc.exceptions import OperationOverflowError, NodeEvaluationError, BinaryOperationError
import textwrap
import ast

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
        elif user_input.lower() == "quit":
            break
        try:
            result = evaluator.evaluate(user_input)
            print(f"Result: {result}")
        except OperationOverflowError:
            print("Err: I can't count to that, sorry.")
        except BinaryOperationError as e:
            if isinstance(e.op, ast.Div):
                if e.left == 0 and e.right == 0:
                    print("Result: Indeterminate.")
                elif e.left != 0 and e.right == 0:
                    print("Result: Undefined.")
            elif isinstance(e.op, (ast.Pow, ast.BitXor)):
                if e.left == 0 and e.right == 0:
                    print("Result: Indeterminate.")
            else:
                print(f"{e.binop_string}")
        except (NodeEvaluationError, SyntaxError) as err:
            print(f"Err: Whoops... Can't answer that ¯\\_(ツ)_/¯")

if __name__ == "__main__":
    main()

