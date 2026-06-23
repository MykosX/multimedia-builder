
# src/models/domain/audio.py

from src.models.core            import BaseModel
from src.models.core.decorators import command
from src.models.providers       import AudioHelper
from src.utils                  import Logger

class AudioModel(BaseModel):
    def __init__(self):
        super().__init__()
    
    # resolves the input as audio: a) read from a file or c) read from cache
    def resolve_audio_input(self, action, audio_path_key="input-audio-path", audio_reference="input-audio-reference") -> AudioHelper:
        input_audio_path            = action.get(audio_path_key)
        input_audio_reference       = action.get(audio_reference)
        
        if input_audio_path:
            audio_data = AudioHelper().load_audio(input_audio_path)
        elif input_audio_reference:
            audio_data = BaseModel.load_from_cache("audio", input_audio_reference)
        else:
            Logger.log_error("PyDubModel", f"No load source specified (file:'{audio_path_key}' or reference:'{audio_reference}').")
            audio_data = AudioHelper()

        return audio_data

    # resolves the output as audio: a) writes to a file or b) saves to cache
    def resolve_audio_output(self, action, audio_data: AudioHelper, audio_path_key="output-audio-path", audio_reference="output-audio-reference"):
        output_audio_path           = action.get(audio_path_key)
        output_audio_reference      = action.get(audio_reference)
        
        if not (output_audio_path or output_audio_reference):
            Logger.log_error("PyDubModel", f"No save target specified (file:'{audio_path_key}' or reference:'{audio_reference}').")
            return

        if output_audio_path:
            audio_data.save_audio(output_audio_path)

        if output_audio_reference:
            BaseModel.save_to_cache("audio", output_audio_reference, audio_data)
    
    # generates a transcript from provided audio
    @command("audio-to-text")
    def audio_to_text(self, action):
        Logger.log_info("AudioModel", "Dummy implementation for 'audio-to-text' command")

    # combines provided audios into one final audio
    @command("merge-audios")
    def merge_audios(self, action):
        Logger.log_info("AudioModel", "Dummy implementation for 'merge-audios' command")

    # creates an audio containing no sounds
    @command("create-silence")
    def create_silence(self, action):
        Logger.log_info("AudioModel", "Dummy implementation for 'create-silence' command")

    # splits provided audio in more audios
    @command("split-audio")
    def split_audio(self, action):
        Logger.log_info("AudioModel", "Dummy implementation for 'split-audio' command")

    # generates speech from provided text
    @command("text-to-speech")
    def text_to_speech(self, action):
        Logger.log_info("AudioModel", "Dummy implementation for 'text-to-speech' command")
