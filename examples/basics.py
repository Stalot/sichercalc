from sichercalc import AstEvaluator

evaluator: AstEvaluator = AstEvaluator()

def main():
    # Creating an arithmetic expression
    expr: str = "0.1+0.2"

    # You can choose between two precision modes: "float" (default) and "decimal"
    float_result: str = evaluator.evaluate(expr)
    decimal_result: str = evaluator.evaluate(expr,
                                             "decimal")
    print(f"float result = {float_result!r}") # '0.30000000000000004'
    print(f"decimal result = {decimal_result!r}") # '0.3'

    # Pick decimal mode if you want fixed-point Decimal precision. You can stick with float if you don't care about float precision issues

if __name__ == "__main__":
    main()
