
# src/models/domain/text.py

from src.models.core            import BaseModel
from src.models.providers       import TextHelper
from src.utils                  import Logger

class TextModel(BaseModel):
    def __init__(self):
        super().__init__()

        self.commands = {
            "translate":            self.translate
        }

    # resolves the input as text: a) direct text, b) read from a file or c) read from cache
    @staticmethod
    def resolve_text_input(action, text_key="text", text_path_key="input-text-path", text_reference="input-text-reference") -> str:
        text                        = action.get(text_key)
        input_text_path             = action.get(text_path_key)
        input_text_reference        = action.get(text_reference)

        if text:
            text_data = text
        elif input_text_path:
            text_data = TextHelper.load_text(input_text_path)
        elif input_text_reference:
            text_data = TextModel.load_from_cache("text", input_text_reference)
        else:
            Logger.log_error("TextModel", f"No text source specified (direct:'{text_key}' or file:'{text_path_key}' or reference:'{text_reference}').")
            text_data = None
            
        return text_data

    # resolves the output as text: a) writes to a file or b) saves to cache
    @staticmethod
    def resolve_text_output(action, text_data: str, text_path_key="output-text-path", text_reference="output-text-reference"):
        output_text_path            = action.get(text_path_key)
        output_text_reference       = action.get(text_reference)

        if not (output_text_path or output_text_reference):
            Logger.log_error("TextModel", f"No save target specified (file:'{text_path_key}' or reference:'{text_reference}').")

        if output_text_path:
            TextHelper.save_text(text_data, output_text_path)

        if output_text_reference:
            TextModel.save_to_cache("text", output_text_reference, text_data)

    # translate command:
    def translate(self, action):
        try:
            Logger.log_info("TextModel", "Translating from text")

            #tts_builder = TTSBuilder()
            #tts_builder.text_to_speech(action).save(action)
        except Exception as e:
            Logger.log_error("TextModel", f"Error in translate: {e}")
