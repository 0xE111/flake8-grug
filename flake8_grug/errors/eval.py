import ast

from . import Error, ErrorCode


def get_error_eval(node: ast.Call) -> Error | None:
    assert isinstance(node, ast.Call)

    if isinstance(node.func, ast.Name) and node.func.id == 'eval':
        return Error(
            lineno=node.lineno,
            col_offset=node.col_offset,
            code=ErrorCode.USING_EVAL,
            snippet=ast.unparse(node),
        )
