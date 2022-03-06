import functools
import os
import sys

from rich.console import Console
from rich.theme import Theme


def format_args(func):
    # print(f'format_args({func!r})')
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        log_level_tag = f"[{func.__name__}]"
        formatted_args = log_level_tag + "\n · ".join(args)
        # print(f'wrapper(log_level_tag = {log_level_tag!r}, formatted_args = {formatted_args!r})')
        return func(self, formatted_args, **kwargs)

    return wrapper


class Logger(Console):
    _theme = {
        "debug": "dim",
        "warn": "yellow",
        "warning": "yellow",
        "error": "red",
        "fatal": "bright_red",
        "success": "green",
        "prompt": "b bright_cyan",
        "title": "b bright_white",
    }

    def __init__(self, **kwargs):
        # print(f'__init__({kwargs!r})')
        PYCHARM_HOSTED = os.getenv("PYCHARM_HOSTED")
        theme = kwargs.get(
            "theme",
            Theme({**self._theme, **{k.upper(): v for k, v in self._theme.items()}}),
        )
        super().__init__(
            # force_terminal=True,
            # log_time_format='[%d.%m.%Y][%T]',
            # safe_box=False,
            # soft_wrap=True,
            log_time=kwargs.get("log_time", False),
            color_system=kwargs.get(
                "color_system", "auto" if PYCHARM_HOSTED else "truecolor"
            ),
            tab_size=kwargs.get("tab_size", 2),
            log_path=kwargs.get("log_path", True),
            file=kwargs.get("file", sys.stdout if PYCHARM_HOSTED else sys.stderr),
            theme=theme,
            width=kwargs.get("width", 160),
        )

    def log_in_out(self, func_or_nothing=None, watch=()):
        """A decorator that logs the entry and exit of a function."""

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                comma_sep_args = ", ".join(map(repr, args))
                comma_sep_kwargs = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
                self.debug(
                    f"➡️️ [b white]Entered[/b white] {func.__name__}({comma_sep_args + comma_sep_kwargs})"
                )
                ret = func(*args, **kwargs)
                self.debug(f"⬅️️️ Exiting {func.__name__}(...) -> {ret!r}")
                return ret

            return wrapper

        if func_or_nothing is None:
            # We're called e.g as @log_in_out()
            return decorator
        # We're called e.g as @log_in_out
        return decorator(func_or_nothing)

    if os.getenv("PDBR_DEBUG", "false").lower() in ("1", "true"):

        @format_args
        def debug(self, *args, **kwargs):
            return self.log(
                *args, _stack_offset=kwargs.pop("_stack_offset", 3), **kwargs
            )

    else:

        def debug(self, *args, **kwargs):
            pass

        print(" ! Logger.debug() disabled\n")

    @format_args
    def info(self, *args, **kwargs):
        return self.log(*args, _stack_offset=kwargs.pop("_stack_offset", 3), **kwargs)

    @format_args
    def warning(self, *args, **kwargs):
        return self.log(*args, _stack_offset=kwargs.pop("_stack_offset", 3), **kwargs)

    @format_args
    def error(self, *args, **kwargs):
        return self.log(*args, _stack_offset=kwargs.pop("_stack_offset", 3), **kwargs)

    @format_args
    def fatal(self, *args, **kwargs):
        return self.log(*args, _stack_offset=kwargs.pop("_stack_offset", 3), **kwargs)

    @format_args
    def success(self, *args, **kwargs):
        return self.log(*args, _stack_offset=kwargs.pop("_stack_offset", 3), **kwargs)

    @format_args
    def prompt(self, *args, **kwargs):
        return self.log(*args, _stack_offset=kwargs.pop("_stack_offset", 3), **kwargs)

    @format_args
    def title(self, *args, **kwargs):
        return self.log(*args, _stack_offset=kwargs.pop("_stack_offset", 3), **kwargs)


log = Logger()
