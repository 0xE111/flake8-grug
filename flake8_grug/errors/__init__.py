from dataclasses import dataclass
from enum import Enum


class ErrorCode(Enum):
    COPY_PASTE = '001', 'Copy-paste of code'
    MISSING_EARLY_QUIT = '002', 'Missing early quie'


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
