import ast

from . import Error, ErrorCode, get_root


def get_error_requests_no_status_check(node: ast.Call) -> Error | None:
    assert isinstance(node, ast.Call)

    # this captures only `res = requests.get/post`, not `from requests import get; get(...)`
    if not (
        isinstance(node.func, ast.Attribute) and
        node.func.value.id == 'requests' and
        node.func.attr in {'get', 'post'}
    ):
        return

    assignment = node.parent
    if not isinstance(assignment, ast.Assign):
        return

    if len(assignment.targets) > 1:
        return

    var = assignment.targets[0]

    try:
        body = assignment.parent.body
    except AttributeError:
        return

    error = Error(
        lineno=var.lineno,
        col_offset=var.col_offset,
        code=ErrorCode.REQUESTS_NO_STATUS_CHECK,
        snippet=ast.unparse(assignment),
    )

    try:
        next_item = next(item for item in body if item.lineno > assignment.lineno)
    except StopIteration:
        return error

    next_line = ast.unparse(next_item)
    if f'{var.id}.raise_for_status()' in next_line or \
       f'{var.id}.ok' in next_line:
       return

    return error

    # , class_or_tuple) node.func.id == 'get':
    # breakpoint()
    # return Error(
    #     lineno=node.lineno,
    #     col_offset=node.col_offset,
    #     code=ErrorCode.USING_EVAL,
    #     snippet=ast.unparse(node),
    # )

    # assert not node.parent
    # code = ast.unparse(node)
    # lines = code.split('\n')

    # for i, line in enumerate(lines[1:], start=1):
    #     line_stripped = line.strip()

    #     if not line_stripped:
    #         continue

    #     if len(line_stripped) <= 7:
    #         continue

    #     if line.startswith('import') or re.match(r'^from .+ import .+$', line):
    #         continue

    #     prev_line = lines[i - 1]

    #     if only_same_length and len(line) != len(prev_line):
    #         continue

    #     with suppress(IndexError):
    #         if prev_line.split(' = ')[1] == line.split(' = ')[1]:
    #             continue

    #     ratio = SequenceMatcher(None, line, prev_line).ratio()
    #     if 1 - ratio < 0.001:  # equal lines are ok
    #         continue

    #     if ratio >= similarity_threshold:
    #         yield Error(lineno=i + 1, col_offset=0, code=ErrorCode.COPY_PASTE, snippet='\n'.join([prev_line, line]))
