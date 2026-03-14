
class NodeError(Exception):
    ...

class ForbiddenNode(NodeError):
    ...

if __name__ == "__main__":
    raise ForbiddenNode("ast.If is forbidden")