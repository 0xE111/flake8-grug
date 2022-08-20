import ast

from . import Error, ErrorCode


def get_error_try_too_much(node: ast.Call, max_lines: int = 3) -> Error | None:
    assert isinstance(node, ast.Try)

    if len(node.body) > max_lines:
        return Error(
            lineno=node.lineno,
            col_offset=node.col_offset,
            code=ErrorCode.TRY_TOO_MUCH,
            snippet=ast.unparse(node),
        )
