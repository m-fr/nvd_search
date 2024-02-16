import functools
import os
import sys
from typing import Callable, ParamSpec, TypeVar

import click
import pydantic

from nvd_search.cli.aliases import cli_aliases
from nvd_search.cli.console import Console
from nvd_search.exceptions import UtilException


class AliasedGroup(click.Group):
    """A click Group subclass that allows for writing aliases and prefixes of any command.
    """
    def get_command(self, ctx: click.core.Context, cmd_name: str):
        """Retrieves the command with the given name.

        If the command is not found, it looks up an explicit command alias or a command prefix.

        Args:
            ctx: The click context object.
            cmd_name: The name of the command to retrieve.

        Returns:
            The command with the given name, or None if no command is found.
        """
        # built-in commands
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # look up an explicit command alias
        if cmd_name in cli_aliases:
            actual_cmd = cli_aliases[cmd_name]
            return click.Group.get_command(self, ctx, actual_cmd)

        # look up a command prefix
        matches = [
            x for x in self.list_commands(ctx) if x.lower().startswith(cmd_name.lower())
        ]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx: click.core.Context, args: list[str]):
        """Resolves the full command's name.
        """
        _, cmd, args = super().resolve_command(ctx, args)
        if cmd is None:
            ctx.fail("No such command")
        return cmd.name, cmd, args


P = ParamSpec("P")
R = TypeVar("R")


def handle_exceptions(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator for pretty printing nvd_search exceptions in debug mode.

    If the exception is a subclass of UtilException and DEBUG environment variable is set to '1', the full exception
    traceback will be printed with local variables shown.
    """
    @functools.wraps(func)
    def outer_function(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, UtilException):
                Console().print(f"[red]Error: {e}")
            if os.environ.get("DEBUG", False):
                Console().print_exception(show_locals=True, suppress=[click, pydantic])
            else:
                Console().print("\n[yellow]Set environment variable [blue]DEBUG=1[/blue] for more details.")
            sys.exit(1)
    return outer_function
