import ast
from dataclasses import dataclass, field

from .errors import Error
from .errors.copy_paste import iter_error_copy_paste
from .errors.early_quit import get_error_early_quit


@dataclass
class Visitor(ast.NodeVisitor):
    errors: list[Error] = field(default_factory=list)

    def visit(self, node: ast.AST):
        if not node.parent:  # root node
            self.errors.extend(iter_error_copy_paste(node))

        super().visit(node)

    def visit_If(self, node: ast.If):
        if error := get_error_early_quit(node):
            self.errors.append(error)
