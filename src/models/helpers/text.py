
# src/models/helpers/text.py

from src.models.core            import BaseHelper
from src.utils                  import Logger, Utils

import whisper

class TextHelper(BaseHelper):
    def __init__(self, text=None):
        self.text = text or ""
    
    def get_text(self) -> str:
        return self.text

    # loads text from specified file path
    def load(self, source_path: str) -> TextHelper:
        try:
            Logger.log_info("TextHelper", f"Loading text from: {source_path}")
            
            with open(source_path, "r", encoding="utf-8") as f:
                self.text = f.read()
        except Exception as e:
            Logger.log_error("TextHelper", f"Error while loading text from {source_path}: {e}")
        
        return TextHelper(self.text)

    # saves text to a specified file
    def save(self, destination_path: str) -> TextHelper:
        try:
            Logger.log_info("TextHelper", f"Saving text to: {destination_path}")
            
            Utils.ensure_dir(destination_path)    
            
            with open(destination_path, "w", encoding="utf-8") as f:
                f.write(self.text)
        except Exception as e:
            Logger.log_error("TextHelper", f"Error while saving text to {destination_path}: {e}")
        
        return self

    # resolves the input as text: a) direct text, b) read from a file or c) read from cache
    def resolve_input(self, input_text, input_text_path, input_text_reference) -> TextHelper:
        if input_text:
            text_helper = TextHelper(input_text)
        elif input_text_path:
            text_helper = TextHelper().load(input_text_path)
        elif input_text_reference:
            text_helper = TextHelper.load_from_cache("text", input_text_reference)
        else:
            Logger.log_error("TextHelper", f"No text source specified (direct:'{input_text}' or file:'{input_text_path}' or reference:'{input_text_reference}').")
            text_helper = TextHelper()
            
        return text_helper

    # resolves the output as text: a) writes to a file or b) saves to cache
    def resolve_output(self, output_text_path, output_text_reference) -> TextHelper:
        if not (output_text_path or output_text_reference):
            Logger.log_error("TextHelper", f"No save target specified (file:'{output_text_path}' or reference:'{output_text_reference}').")

        if output_text_path:
            self.save(output_text_path)

        if output_text_reference:
            TextHelper.save_to_cache("text", output_text_reference, self)
        
        return self

    def audio_to_text(self, input_audio_path, model_settings) -> TextHelper:
        model = whisper.load_model(model_settings["whisper-model"])
        result = model.transcribe(input_audio_path, word_timestamps=True)

        words_info = []
        for segment in result['segments']:
            for word_info in segment['words']:
                words_info.append({
                    'word': word_info['word'],
                    'start_time': word_info['start'],
                    'end_time': word_info['end']
                })

        # Format each word as a separate subtitle line
        transcript_text = ""
        for i, word_info in enumerate(words_info, 1):
            start_time  = Utils.format_time(word_info['start_time'])
            end_time    = Utils.format_time(word_info['end_time'])
            word = word_info['word'].strip()
            transcript_text += f"{i}\n{start_time} --> {end_time}\n{word}\n\n"
        
        self.text = transcript_text
        
        return self
