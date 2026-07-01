
# src/models/domain/audio.py

from pathlib import Path

from src.models.core            import BaseModel
from src.models.core.decorators import command
from src.models.helpers         import AudioHelper, TextHelper
from src.utils                  import Logger, Utils

class AudioModel(BaseModel):
    def __init__(self):
        super().__init__()
    
    def get_coqui_settings(self, action):
        model_settings = {
            "coqui-model-path"  : action.get("coqui-model-path", None),
            "speed"             : action.get("speech-speed", 1.0),
            "energy"            : action.get("speech-energy", 1.0),
            "speaker"           : action.get("speech-speaker", None),
            "speaker_wav"       : action.get("input-voice-path", None),
            "language"          : action.get("language", None)
        }
        return model_settings

    def get_whisper_settings(self, action):
        model_settings = {
            "whisper-model":    action.get("whisper-model")
        }
        return model_settings

    # generates a transcript from provided audio
    @command("audio-to-text")
    def audio_to_text(self, action):
        input_audio_path            = action.get("input-audio-path")
        input_audio_reference       = action.get("input-audio-reference")
        
        output_text_path            = action.get("output-text-path")
        output_text_reference       = action.get("output-text-reference")

        try:
            Logger.log_info("AudioModel", "Generating transcript from audio")
            
            if input_audio_path is None:
                temp_file_path = output_text_path + ".wav"
                AudioHelper().resolve_input(input_audio_path, input_audio_reference).save(temp_file_path)
            else:
                temp_file_path = input_audio_path

            text_helper = TextHelper().audio_to_text(temp_file_path, self.get_whisper_settings(action))
            
            if input_audio_path is None:
                Utils.delete_file(temp_file_path)
                
            text_helper.resolve_output(output_text_path, output_text_reference)

        except Exception as e:
            Logger.log_error("AudioModel", f"Error in audio-to-text: {e}")

    # combines provided audios into one final audio
    @command("merge-audios")
    def merge_audios(self, action):
        input_audio_paths           = action.get("input-audio-paths")
        input_audio_references      = action.get("input-audio-references")
        output_audio_path           = action.get("output-audio-path")
        output_audio_reference      = action.get("output-audio-reference")

        try:
            Logger.log_info("AudioModel", "Starting merging audios")
            
            audio_helpers: list[AudioHelper] = []
            
            # Load audio from file paths
            if input_audio_paths:
                for file_path in input_audio_paths:
                    audio_helpers.append(AudioHelper().resolve_input(file_path, None))

            # Load audio from cache
            if input_audio_references:
                for audio_reference in input_audio_references:
                    audio_helpers.append(AudioHelper().resolve_input(None, audio_reference))
            
            if not audio_helpers:
                Logger.log_error("AudioModel", "No valid audio inputs for merge")
                return

            audio_helper = AudioHelper().merge(audio_helpers)

            audio_helper.resolve_output(output_audio_path, output_audio_reference)

        except Exception as e:
            Logger.log_error("AudioModel", f"Error in merge-audios: {e}")

    # creates an audio containing no sounds
    @command("with-silence")
    def create_silence(self, action):
        input_audio_path            = action.get("input-audio-path")
        input_audio_reference       = action.get("input-audio-reference")
        duration                    = action.get("duration", 1.0)
        output_audio_path           = action.get("output-audio-path")
        output_audio_reference      = action.get("output-audio-reference")

        try:
            Logger.log_info("AudioModel", "Adding silence")
            
            audio_helper = AudioHelper()
            
            #can add silence to existing audio
            if input_audio_path or input_audio_reference:
                audio_helper.resolve_input(input_audio_path, input_audio_reference)
            
            # or just create silence
            audio_helper.with_silence(duration)
            audio_helper.resolve_output(output_audio_path, output_audio_reference)

        except Exception as e:
            Logger.log_error("AudioModel", f"Error in with-silence: {e}")

    # splits provided audio in more audios
    @command("split-audio")
    def split_audio(self, action):
        input_audio_path            = action.get("input-audio-path")
        input_audio_reference       = action.get("input-audio-reference")
        split_times                 = action.get("split-times", [])
        output_audio_path           = action.get("output-audio-path")
        
        try:
            Logger.log_info("AudioModel", "Splitting audio file")
            
            audio_helper = AudioHelper().resolve_input(input_audio_path, input_audio_reference)
            chunks = audio_helper.split(split_times)
            
            p = Path(output_audio_path)
            for index, chunk in enumerate(chunks, start=1):
                part_path = p.parent / f"{p.stem}-part{index}{p.suffix}"
                chunk.save(str(part_path))

        except Exception as e:
            Logger.log_error("AudioModel", f"Error in split-audio: {e}")

    # generates speech from provided text
    @command("text-to-speech")
    def text_to_speech(self, action):
        input_text                  = action.get("text")
        input_text_path             = action.get("input-text-path")
        
        output_audio_path           = action.get("output-audio-path")
        output_audio_reference      = action.get("output-audio-reference")

        try:
            Logger.log_info("AudioModel", "Generating speech from text")
            
            text = TextHelper().resolve_input(input_text, input_text_path, None).get_text()
            audio_helper = AudioHelper().text_to_speech(text, self.get_coqui_settings(action), output_audio_path)
            audio_helper.resolve_output(output_audio_path, output_audio_reference)
            
        except Exception as e:
            Logger.log_error("AudioModel", f"Error in text-to-speech: {e}")

    # runs custom commands from specific tts's
    @command("run-custom")
    def run_custom(self, action):
        Logger.log_info("AudioModel", "Dummy implementation for 'run-custom' command")
