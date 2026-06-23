
# -----------------------------------------------------------------------------
# src/model/text_model.py
# -----------------------------------------------------------------------------

from src.core               import command, Logger
from src.model              import BaseModel
from src.model.helper       import TextHelper

# -----------------------------------------------------------------------------
# TextModel
#
# * Gives access to all usable text commands
# * Has the ability to access the JSON configuration with convenient
# python functions and names
# -----------------------------------------------------------------------------


class TextModel(BaseModel):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self):
        super().__init__()

    # -------------------------------------------------------------------------
    # General text transformations
    # -------------------------------------------------------------------------

    @command("translate")
    def translate(self, ctx):
        Logger.info(
            self,
            "Dummy implementation for 'translate' command"
        )

# -----------------------------------------------------------------------------
