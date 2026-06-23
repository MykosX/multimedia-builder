
from src.models.domain  import AudioModel, ImageModel, VideoModel, TextModel

class ActivityExecutor:
    def __init__(self, logger):
        self.logger = logger

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
            self.logger.error(f"Unknown handler type: {type_}")
            return

        handler = handler_class()

        try:
            handler.run(activity)
        except Exception as e:
            self.logger.error(f"Execution failed: {e}")
