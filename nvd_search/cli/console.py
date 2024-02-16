from rich.console import Console as RichConsole

from nvd_search.singleton import Singleton  # type: ignore[attr-defined]


class Console(RichConsole, metaclass=Singleton):
    """Singleton wrapper around Rich's Console."""
