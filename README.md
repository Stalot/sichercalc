# sichercalc

Fork of [ast_calculator](https://github.com/mrfuxi/ast_calculator), modernized and refactored as a reusable library.

## What is SicherCalc?

When you need to evaluate simple mathematical or logical expressions supplied by
untrusted users, you need a sandboxed environment that prevents arbitrary code
execution. SafeCalc parses the expression into an abstract syntax tree (AST),
inspects each node, and evaluates only those that belong to a predefined,
whitelisted set of operations.

### Why AST?

An abstract syntax tree (AST) is a tree‑structured representation of source code.
By operating on the AST we can precisely control which constructs are allowed,
eliminating the security risks associated with `eval()`.

## Features

- No `eval()` – pure AST parsing and controlled evaluation  
- Extensible – register your own custom functions  
- Works on Python 3.10+

## Getting Started

### Installation

```bash
pip install sichercalc
```
