
# -----------------------------------------------------------------------------
# src/file/base_file.py
# -----------------------------------------------------------------------------

from typing                 import Self

from src.core               import BaseNode, Console, FileHandler

# -----------------------------------------------------------------------------
# BaseFile
#
# * Creates standard interfaces for reading from files and writing to files
# -----------------------------------------------------------------------------


class BaseFile:
    # -------------------------------------------------------------------------
    # Class properties
    # -------------------------------------------------------------------------

    CACHE_DIR: str      = "/dev/shm/multimedia-builder"
    CACHE_TYPE: str     = "base"

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, resource=None):
        self.resource = resource

    # -------------------------------------------------------------------------
    # General IO with files
    # -------------------------------------------------------------------------

    @classmethod
    def from_file(cls, source_path: str) -> Self:
        pass

    def to_file(self, destination_path: str) -> None:
        pass

    @classmethod
    def from_cache(cls, data_reference: str) -> Self:
        source_reference = f"{cls.CACHE_DIR}/{data_reference}"
        return cls.from_file(source_reference)

    def to_cache(self, data_reference: str) -> None:
        destination_reference = f"{self.CACHE_DIR}/{data_reference}"
        FileHandler.ensure_dir(destination_reference)
        return self.to_file(destination_reference)

    # -------------------------------------------------------------------------
    # IO wrappers
    # -------------------------------------------------------------------------

    @classmethod
    def find_source(cls, source_path: BaseNode, data_reference: BaseNode) -> str:
        if source_path:
            return f"{source_path}"
        elif data_reference:
            return f"{cls.CACHE_DIR}/{data_reference}"
        else:
            return None

    @classmethod
    def from_source(cls, source_path: BaseNode, data_reference: BaseNode, required: bool = True) -> Self:
        if source_path:
            return cls.from_file(f"{source_path}")
        elif data_reference:
            return cls.from_cache(f"{data_reference}")
        else:
            message = f"No load source specified (file:'{source_path.json_name}' or reference:'{data_reference.json_name}')"

            if required:
                raise Exception(message)
            else:
                Console.warning(message)
                return cls()

    @classmethod
    def find_destination(cls, destination_path: BaseNode, data_reference: BaseNode) -> str:
        if destination_path:
            return f"{destination_path}"
        elif data_reference:
            return f"{cls.CACHE_DIR}/{data_reference}"
        else:
            return None

    def to_destination(self, destination_path: BaseNode, data_reference: BaseNode, required: bool = True) -> None:
        if destination_path:
            FileHandler.ensure_dir(f"{destination_path}")
            self.to_file(f"{destination_path}")
        if data_reference:
            self.to_cache(f"{data_reference}")
        if not (destination_path or data_reference):
            message = f"No save target specified (file:'{destination_path.json_name}' or reference:'{data_reference.json_name}')"

            if required:
                raise Exception(message)
            else:
                Console.warning(message)

    # -------------------------------------------------------------------------
    # cache clean-up
    # -------------------------------------------------------------------------

    @classmethod
    def cache_cleanup(cls) -> None:
        FileHandler.delete(f"{cls.CACHE_DIR}")

# -----------------------------------------------------------------------------
