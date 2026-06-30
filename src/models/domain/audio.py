
# src/models/domain/audio.py

from src.models.core            import BaseModel
from src.models.core.decorators import command
from src.models.helpers         import AudioHelper, TextHelper
from src.utils                  import Logger

class AudioModel(BaseModel):
    def __init__(self):
        super().__init__()
    
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
        input_audio_path            = action.get("input-audio-path")
        input_audio_reference       = action.get("input-audio-reference")
        split_times                 = action.get("split-times", [])
        output_audio_path           = action.get("output-audio-path")
        
        try:
            Logger.log_info("AudioModel", "Spliting audio in more audios")
            
            audio_helper = AudioHelper().resolve_audio_input(input_audio_path, input_audio_reference)
            audio_helper.split_audio(split_times, output_audio_path)

        except Exception as e:
            Logger.log_error("AudioModel", f"Error in split-audio: {e}")

    # generates speech from provided text
    @command("text-to-speech")
    def text_to_speech(self, action):
        input_text                  = action.get("text")
        input_text_path             = action.get("input-text-path")
        input_text_reference        = action.get("input-text-reference")
        speech_speed                = action.get("speech-speed", 1.0)
        speech_energy               = action.get("speech-energy", 1.0)
        speech_speaker              = action.get("speech-speaker", None)
        input_voice_path            = action.get("input-voice-path", None)
        tts_model_path              = action.get("tts-model-path", None)
        language                    = action.get("language", None)
        output_audio_path           = action.get("output-audio-path")
        output_audio_reference      = action.get("output-audio-reference")

        try:
            Logger.log_info("AudioModel", "Generating speech from text")
            
            text = TextHelper().resolve_text_input(input_text, input_text_path, input_text_reference).get_text()
            
            tts_settings = {
                "model_path"        : tts_model_path,
                "speed"             : speech_speed,
                "energy"            : speech_energy,
                "speaker"           : speech_speaker,
                "speaker_wav"       : input_voice_path,
                "language"          : language
            }
            audio_helper = AudioHelper().text_to_speech(text, tts_settings, output_audio_path)
            audio_helper.resolve_audio_output(output_audio_path, output_audio_reference)
            
        except Exception as e:
            Logger.log_error("AudioModel", f"Error in text-to-speech: {e}")

    # runs custom commands from specific tts's
    @command("run-custom")
    def run_custom(self, action):
        Logger.log_info("AudioModel", "Dummy implementation for 'run-custom' command")
