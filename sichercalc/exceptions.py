
class ForbiddenNode(Exception):
    ...

if __name__ == "__main__":
    raise ForbiddenNode("ast.If is forbidden")