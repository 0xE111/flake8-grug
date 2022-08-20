import ast
import re
from contextlib import suppress
from difflib import SequenceMatcher
from typing import Iterator

from . import Error, ErrorCode


def iter_error_copy_paste(
    node: ast.AST,
    similarity_threshold: float = 0.9,
    only_same_length: bool = True,
) -> Iterator[Error]:


    assert not node.parent
    code = ast.unparse(node)
    lines = code.split('\n')

    for i, line in enumerate(lines[1:], start=1):
        line_stripped = line.strip()

        if not line_stripped:
            continue

        if len(line_stripped) <= 7:
            continue

        if line.startswith('import') or re.match(r'^from .+ import .+$', line):
            continue

        prev_line = lines[i - 1]

        if only_same_length and len(line) != len(prev_line):
            continue

        with suppress(IndexError):
            if prev_line.split(' = ')[1] == line.split(' = ')[1]:
                continue

        ratio = SequenceMatcher(None, line, prev_line).ratio()
        if 1 - ratio < 0.001:  # equal lines are ok
            continue

        if ratio >= similarity_threshold:
            yield Error(lineno=i + 1, col_offset=0, code=ErrorCode.COPY_PASTE, snippet='\n'.join([prev_line, line]))
