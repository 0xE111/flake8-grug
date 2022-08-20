import ast
from dataclasses import dataclass, field
from enum import Enum


class ErrorCode(Enum):
    COPY_PASTE = '001', 'Copy-paste of code'


@dataclass
class Error:
    PREFIX = 'GRG'

    lineno: int
    col_offset: int
    code: ErrorCode

    @property
    def message(self) -> str:
        return self.PREFIX + self.code.value[0] + ' ' + self.code.value[1]


@dataclass
class Visitor(ast.NodeVisitor):
    errors: list[Error] = field(default_factory=list)

    def __post_init__(self):
        self.errors = [Error(lineno=1, col_offset=0, code=ErrorCode.COPY_PASTE)]

    # def visit_Assign(self, node: ast.Assign) -> None:  # noqa: N802
    #     self.errors.extend(check_deprecated_typing(node))
    #     self.generic_visit(node)

    #  (node.lineno, node.col_offset, T100)
