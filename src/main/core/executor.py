
# src/main/core/executor.py

from src.models.domain          import AudioModel, ImageModel, VideoModel, TextModel
from src.utils                  import Logger

class ActivityExecutor:
    def __init__(self):
        self.registry = {
            "audio":        AudioModel,
            "image":        ImageModel,
            "video":        VideoModel,
            "text":         TextModel
        }

    def execute(self, activity):
        type_ = activity.get("type")
        handler_class = self.registry.get(type_)

        if not handler_class:
            Logger.log_error("ActivityExecutor", f"Unknown handler type: {type_}")
            return

        handler = handler_class()

        try:
            handler.run(activity)
        except Exception as e:
            Logger.log_error("ActivityExecutor", f"Execution failed: {e}")
