
# -----------------------------------------------------------------------------
# src/model/helper/text_helper.py
# -----------------------------------------------------------------------------

from typing                 import Self

# -----------------------------------------------------------------------------
# TextHelper
#
# * Provides access to text transformations
# -----------------------------------------------------------------------------


class TextHelper:
    # -------------------------------------------------------------------------
    # General text transformations
    # -------------------------------------------------------------------------

    @staticmethod
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

    @classmethod
    def from_timestamped(cls, items: list[dict]) -> Self:
        text = ""

        for i, item in enumerate(items, 1):
            text += (
                f"{i}\n"
                f"{TextHelper.format_time(item['start_time'])} --> "
                f"{TextHelper.format_time(item['end_time'])}\n"
                f"{item['text']}\n\n"
            )
        return cls(text)

# -----------------------------------------------------------------------------
