
# -----------------------------------------------------------------------------
# src/file/json_file.py
# -----------------------------------------------------------------------------

import json

from typing                 import Self

from src.file              import BaseFile

# -----------------------------------------------------------------------------
# JsonFile
#
# * Gives access to reading and writing JSON files
# -----------------------------------------------------------------------------


class JsonFile(BaseFile):
    # -------------------------------------------------------------------------
    # Access to json property
    # -------------------------------------------------------------------------

    @property
    def json(self):
        return self.resource

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, json = None):
        super().__init__(json)

    # -------------------------------------------------------------------------
    # IO access to json files
    # -------------------------------------------------------------------------

    @classmethod
    def from_file(cls, source_path: str) -> Self:
        with open(source_path, encoding="utf-8") as f:
            return cls(
                json.load(f)
            )

        return cls()

    def to_file(self, destination_path: str) -> None:
        with open(destination_path, "w", encoding="utf-8") as file:
            json.dump(
                self.json,
                file,
                indent=4,
                ensure_ascii=False
            )

# -----------------------------------------------------------------------------
