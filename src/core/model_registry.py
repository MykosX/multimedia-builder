
# -----------------------------------------------------------------------------
# src/core/model_registry.py
# -----------------------------------------------------------------------------

from src.core               import BaseNode, Logger
from src.model              import AudioModel, ImageModel, TextModel, VideoModel

# -----------------------------------------------------------------------------
# ModelRegistry
#
# * Makes sure the appropriate model is configured and it can execute commands
# -----------------------------------------------------------------------------


class ModelRegistry:
    # -------------------------------------------------------------------------
    # Class properties
    # -------------------------------------------------------------------------

    REGISTRY = {
        "audio"     : AudioModel,
        "image"     : ImageModel,
        "text"      : TextModel,
        "video"     : VideoModel
    }

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self):
        pass

    # -------------------------------------------------------------------------
    # Run
    # -------------------------------------------------------------------------

    @classmethod
    def run(cls, model_name: str, context: BaseNode):
        model_class = cls.REGISTRY.get(model_name)

        if model_class:
            Logger.debug(
                cls,
                f"Executing {model_class.__name__}"
            )

            model_class().run(context)
        else:
            Logger.error(
                cls,
                f"Model '{model_name}' is unavailable"
            )

# -----------------------------------------------------------------------------
