# Standard Library
import logging
import logging.config
import sys
from time import gmtime

from colorlog import ColoredFormatter


logging.Formatter.converter = gmtime

_fmt = "%(asctime)s,%(msecs)03d - %(levelname)s (%(process)d) [%(name)s:%(lineno)d] %(message)s"
_datefmt = "%Y-%m-%dT%H:%M:%S"

_handler = logging.StreamHandler(sys.stdout)
# _formatter = logging.Formatter(fmt=_fmt, datefmt=_datefmt)
_colored_formatter = ColoredFormatter(
    fmt="%(log_color)s{}".format(_fmt),
    datefmt=_datefmt,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_yellow",
    },
)
_handler.setLevel(logging.DEBUG)
_handler.setFormatter(_colored_formatter)


class LoggerBuilder(object):
    def __init__(self, context: str) -> None:
        self._logger = logging.getLogger(context)
        self._logger.propagate = False

    def add_handler(self, handler: logging.Handler) -> "LoggerBuilder":
        self._logger.addHandler(handler)
        return self

    def set_level(self, level: int = logging.INFO) -> "LoggerBuilder":
        self._logger.setLevel(level)
        return self

    def build(self):
        return self._logger


def get_logger(context: str, level: int = logging.DEBUG) -> logging.Logger:
    builder = LoggerBuilder(context=context)
    logger = builder.set_level(level).add_handler(_handler).build()

    return logger
