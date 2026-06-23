
# -----------------------------------------------------------------------------
# src/core/logging.py
# -----------------------------------------------------------------------------

from pathlib                import Path
from datetime               import datetime
from time                   import perf_counter
from typing                 import Type
import warnings

from colorama               import Fore, Style, init as colorama_init

# -----------------------------------------------------------------------------
# Logger
#
# * Logs various messages to file
# -----------------------------------------------------------------------------


class Logger:
    # -------------------------------------------------------------------------
    # Class properties
    # -------------------------------------------------------------------------
    LOG_FILE_PATH = None

    @classmethod
    def timestamp(cls, format="%Y-%m-%d %H:%M:%S") -> str:
        return f"{datetime.now():{format}}"

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        warnings.showwarning = Logger.show_warning

        Path("logs").mkdir(exist_ok=True)

        Logger.LOG_FILE_PATH = (
            f"logs/run_{Logger.timestamp('%Y-%m-%d_%H-%M-%S')}.log"
        )

        Logger.info(
            Logger,
            f"Logger initialized. Saving logs to {Logger.LOG_FILE_PATH}"
        )

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @classmethod
    def resolve_name(cls, source):
        if source is None:
            return "Unknown"

        if isinstance(source, str):
            return source

        if isinstance(source, type):
            return source.__name__

        return type(source).__name__

    @classmethod
    def write_file(cls, line: str) -> None:
        with open(cls.LOG_FILE_PATH, "a", encoding="utf-8") as file:
            file.write(line + "\n")

    @classmethod
    def write(cls, level: str, source, message: str) -> None:
        name = cls.resolve_name(source)

        line = f"[{level}] [{name}] {message}"

        cls.write_file(
            f"{cls.timestamp()} {line}"
        )

    @classmethod
    def show_warning(
        cls,
        message,
        category,
        filename,
        lineno,
        file=None,
        line=None,
    ):
        cls.write(
            "WARNING",
            Path(filename).parts[-2],
            f"{category.__name__}: {message}"
        )

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    @classmethod
    def debug(cls, source, message) -> None:
        cls.write("DEBUG", source, message)

    @classmethod
    def info(cls, source, message) -> None:
        cls.write("INFO", source, message)

    @classmethod
    def warning(cls, source, message) -> None:
        cls.write("WARNING", source, message)

    @classmethod
    def error(cls, source, message) -> None:
        cls.write("ERROR", source, message)

# -----------------------------------------------------------------------------
# Console
#
# * Logs messages to console
# * Sends messages to Logger
# -----------------------------------------------------------------------------


class Console(Logger):
    # -------------------------------------------------------------------------
    # Class properties
    # -------------------------------------------------------------------------

    COLORS = {
        "INFO": Fore.WHITE,
        "DEBUG": Fore.CYAN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
    }

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:
        super().initialize()
        colorama_init(autoreset=True)

    # -------------------------------------------------------------------------
    # Console helpers
    # -------------------------------------------------------------------------

    @classmethod
    def write_console(cls, level: str, line: str) -> None:
        color = cls.COLORS.get(level, Fore.WHITE)

        print(f"{color}{line}{Style.RESET_ALL}")

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    @classmethod
    def message(cls, level: str, message: str) -> None:
        cls.write_console(
            level,
            f"[{level}] {message}"
        )

        super().write(
            level,
            cls,
            message
        )

    @classmethod
    def debug(cls, message) -> None:
        cls.message("DEBUG", message)

    @classmethod
    def info(cls, message) -> None:
        cls.message("INFO", message)

    @classmethod
    def warning(cls, message) -> None:
        cls.message("WARNING", message)

    @classmethod
    def error(cls, message) -> None:
        cls.message("ERROR", message)

# -----------------------------------------------------------------------------
