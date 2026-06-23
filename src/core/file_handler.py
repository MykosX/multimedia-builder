
# -----------------------------------------------------------------------------
# src/core/file_context.py
# -----------------------------------------------------------------------------

import shutil

from abc                    import ABC
from pathlib                import Path
from typing                 import Self

# -----------------------------------------------------------------------------
# FileHandler
#
# * Gives access to path operations
# -----------------------------------------------------------------------------


class FileHandler(ABC):
    # -------------------------------------------------------------------------
    # Path helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def exists(path: str) -> bool:
        return Path(path).exists()

    @staticmethod
    def is_file(path: str) -> bool:
        return Path(path).is_file()

    @staticmethod
    def is_directory(path: str) -> bool:
        return Path(path).is_dir()

    @staticmethod
    def parent(path: str) -> str:
        return str(Path(path).parent)

    @staticmethod
    def filename(path: str) -> str:
        return Path(path).name

    @staticmethod
    def stem(path: str) -> str:
        return Path(path).stem

    @staticmethod
    def extension(path: str) -> str:
        return Path(path).suffix

    @staticmethod
    def join(*parts: str) -> str:
        return str(Path(*parts))

    @staticmethod
    def absolute(path: str) -> str:
        return str(Path(path).resolve())

    # -------------------------------------------------------------------------
    # File system helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def ensure_dir(path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def delete(path: str) -> None:
        path = Path(path)

        if not path.exists():
            return

        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

# -----------------------------------------------------------------------------
