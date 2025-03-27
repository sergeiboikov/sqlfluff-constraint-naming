"""SQLFluff plugin for Postgres constraint naming conventions."""

__version__ = "0.1.0"

from typing import List, Type
from sqlfluff.core.plugin import hookimpl
from sqlfluff.core.rules import BaseRule


@hookimpl
def get_rules() -> List[Type[BaseRule]]:
    """Get plugin rules.

    Returns:
        A list of rule classes to be registered with SQLFluff.
    """
    from .rules import Rule_CN01
    return [Rule_CN01]
