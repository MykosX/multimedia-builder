
# src/models/domain/text.py

from src.models.core            import BaseModel
from src.models.helpers         import TextHelper
from src.utils                  import Logger

class TextModel(BaseModel):
    def __init__(self):
        super().__init__()

        self.commands = {
            "translate":            self.translate
        }

    # translate command:
    def translate(self, action):
        try:
            Logger.log_info("TextModel", "Translating from text")

            #tts_builder = TTSBuilder()
            #tts_builder.text_to_speech(action).save(action)
        except Exception as e:
            Logger.log_error("TextModel", f"Error in translate: {e}")
