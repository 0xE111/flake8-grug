import ast

from . import Error, ErrorCode


def get_error_early_quit(node: ast.If, max_else_lines: int = 3) -> Error | None:
    assert isinstance(node, ast.If)
    if isinstance(node.orelse, ast.If):  # if second "if"
        return

    if len(node.orelse) > max_else_lines:
        return

    if isinstance(node.orelse[-1], (ast.Return, ast.Raise)):
        return Error(
            lineno=node.lineno,
            col_offset=node.col_offset,
            code=ErrorCode.MISSING_EARLY_QUIT,
            snippet=ast.unparse(node),
        )
