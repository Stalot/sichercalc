from sichercalc import AstEvaluator

evaluator = AstEvaluator()

def circle_area(r, pi: None | float = None):
    if not pi:
        pi = 3.14
    return (r**2)*pi

def main():
    expr: str = "circle_area(radius, pi)"

    context = {
            "constants": {
                "pi":  3.1415,
                "radius": 6.25
            },
            "functions": {
                "circle_area": circle_area
            }
    }

    result: str = evaluator.evaluate(expr,
                                     "decimal",
                                     context)
    print(f"result = {result}") # 122.71484375

if __name__ == "__main__":
    main()
