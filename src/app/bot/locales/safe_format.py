from html import escape
from string import Formatter
from typing import Any


class SafeFormat:
    def __init__(self, text: str):
        self.text = text

    def format(self, **kwargs: Any) -> str:
        escaped_kwargs = {k: self._escape(v) for k, v in kwargs.items()}
        return Formatter().vformat(self.text, (), escaped_kwargs)

    def __str__(self) -> str:
        return self.text

    @staticmethod
    def _escape(value: Any) -> str:
        if isinstance(value, str):
            return escape(value)
        return str(value)
