import ast
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from enum import Enum
from typing import Iterator


class ErrorCode(Enum):
    COPY_PASTE = '001', 'Copy-paste of code'


@dataclass
class Error:
    PREFIX = 'GRG'

    lineno: int
    col_offset: int
    code: ErrorCode
    description: str = ''

    @property
    def message(self) -> str:
        return self.PREFIX + self.code.value[0] + ' ' + self.code.value[1] + ' ' + self.description


@dataclass
class Visitor(ast.NodeVisitor):
    errors: list[Error] = field(default_factory=list)

    def visit(self, node: ast.AST):
        if not node.parent:  # root node
            self.errors.extend(iter_error_copy_paste(node))

        super().visit(node)

    # def visit_Assign(self, node: ast.Assign) -> None:  # noqa: N802
    #     self.errors.extend(check_deprecated_typing(node))
    #     self.generic_visit(node)

    #  (node.lineno, node.col_offset, T100)


def iter_error_copy_paste(node: ast.AST) -> Iterator[Error]:
    assert not node.parent
    SIMILARITY_THRESHOLD = 0.7
    LOOKBACK_LINES = 4

    code = ast.unparse(node)
    lines = [line.strip() for line in code.split('\n')]

    for i, line in enumerate(lines):
        if not line:
            continue

        for prev_line in lines[max(0, i - LOOKBACK_LINES):i]:
            if line == prev_line:
                breakpoint()
            if SequenceMatcher(None, line, prev_line).ratio() >= SIMILARITY_THRESHOLD:
                yield Error(lineno=i, col_offset=0, code=ErrorCode.COPY_PASTE, description=f'{prev_line=}, {line=}')
