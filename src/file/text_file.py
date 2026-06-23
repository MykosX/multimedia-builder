
# -----------------------------------------------------------------------------
# src/file/text_file.py
# -----------------------------------------------------------------------------

from typing                 import Self

from src.core               import Console, Logger
from src.file               import BaseFile

# -----------------------------------------------------------------------------
# JsonFile
#
# * Gives access to reading and writing text files
# -----------------------------------------------------------------------------


class TextFile(BaseFile):
    # -------------------------------------------------------------------------
    # Access to text property
    # -------------------------------------------------------------------------

    @property
    def text(self):
        return self.resource

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, text = None):
        super().__init__(text)

    # -------------------------------------------------------------------------
    # IO access to text files
    # -------------------------------------------------------------------------

    @classmethod
    def from_file(cls, source_path: str) -> Self:
        with open(source_path, "r", encoding="utf-8") as f:
            return cls(
                f.read()
            )

        return cls()

    def to_file(self, destination_path: str) -> None:
        Logger.info(
            type(self),
            f"Saving text to {destination_path.json_name} = {destination_path}"
        )

        with open(destination_path, "w", encoding="utf-8") as f:
            f.write(self.text)

    # -------------------------------------------------------------------------
    # IO wrappers
    # -------------------------------------------------------------------------

    @classmethod
    def from_source(cls, text: BaseNode, input_text_path: BaseNode, input_text_reference: BaseNode, required: bool = True) -> Self:
        if text:
            return cls(text.get())

        Console.warning(f"No direct text provided: {text.json_name}, checking {input_text_path.json_name} and {input_text_reference.json_name}.")
        return super().from_source(
            input_text_path,
            input_text_reference,
            required
        )

# -----------------------------------------------------------------------------
