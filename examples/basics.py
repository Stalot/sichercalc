from sichercalc import AstEvaluator

evaluator: AstEvaluator = AstEvaluator()

def main():
    # Creating an arithmetic expression
    expr: str = "0.1+0.2"

    decimal_result: str = evaluator.evaluate(expr)
    print(f"{decimal_result!r}") # '0.3000000000000000166533453694'

if __name__ == "__main__":
    main()
