import ast
from dataclasses import dataclass
from enum import Enum


class ErrorCode(Enum):
    COPY_PASTE = '001', 'Copy-paste of code'
    MISSING_EARLY_QUIT = '002', 'Missing early quit'
    USING_EVAL = '003', 'Using eval'
    TRY_TOO_MUCH = '004', 'Too big "try" code block'
    REQUESTS_NO_STATUS_CHECK = '005', 'Not checking response status code'


@dataclass
class Error:
    PREFIX = 'GRG'

    lineno: int
    col_offset: int
    code: ErrorCode
    snippet: str = ''

    @property
    def message(self) -> str:
        return self.PREFIX + self.code.value[0] + ' ' + self.code.value[1]


def get_root(node: ast.AST) -> ast.AST:
    while (parent := node.parent) is not None:
        node = parent

    return node
