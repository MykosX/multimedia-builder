
# src/models/providers/audio.py

from pydub                      import AudioSegment

from src.models.core            import BaseHelper
from src.utils                  import Logger, Utils

from TTS.api                    import TTS

class AudioHelper(BaseHelper):
    def __init__(self, audio_segment=None):
        self.audio_segment = audio_segment or AudioSegment.silent(0)

    def get_audio(self) -> AudioSegment:
        return self.audio_segment

    # loads an audio file from specified source
    def load_audio(self, source_path) -> AudioHelper:
        try:
            Logger.log_info("AudioHelper", f"Loading audio from: {source_path}")

            self.audio_segment = AudioSegment.from_file(source_path)

        except Exception as e:
            Logger.log_error("AudioHelper", f"Error while loading audio: {e}")
            self.audio_segment = AudioSegment.silent(0)

        return self

    # saves provided audio file to specified destination
    def save_audio(self, destination_path, format="wav") -> AudioHelper:
        try:
            Logger.log_info("AudioHelper", f"Saving audio to: {destination_path}")

            Utils.ensure_dir(destination_path)

            self.audio_segment.export(destination_path, format=format)

        except Exception as e:
            Logger.log_error("AudioHelper", f"Error while saving audio: {e}")

        return self

    # resolves the input as audio: a) read from a file or c) read from cache
    def resolve_audio_input(self, action, audio_path_key="input-audio-path", audio_reference="input-audio-reference") -> AudioHelper:
        input_audio_path            = action.get(audio_path_key)
        input_audio_reference       = action.get(audio_reference)
        
        if input_audio_path:
            audio_data = AudioHelper().load_audio(input_audio_path)
        elif input_audio_reference:
            audio_data = AudioHelper.load_from_cache("audio", input_audio_reference)
        else:
            Logger.log_error("AudioHelper", f"No load source specified (file:'{audio_path_key}' or reference:'{audio_reference}').")
            audio_data = AudioHelper()

        return audio_data

    # resolves the output as audio: a) writes to a file or b) saves to cache
    def resolve_audio_output(self, output_audio_path, output_audio_reference) -> AudioHelper:
        if not (output_audio_path or output_audio_reference):
            Logger.log_error("AudioHelper", f"No save target specified (file:'{output_audio_path}' or reference:'{output_audio_reference}').")
            return

        if output_audio_path:
            self.save_audio(output_audio_path)

        if output_audio_reference:
            AudioHelper.save_to_cache("audio", output_audio_reference, self)
        
        return self

    # generates speech with Coqui TTS
    def text_to_speech(self, text, tts_settings, output_audio_path) -> AudioHelper:
        model_path = tts_settings["model_path"] or "tts_models/en/ljspeech/vits"
        
        Logger.log_info("AudioHelper", f"Initialized Coqui TTS model: {model_path}")
        coqui_tts = TTS(model_path)
        
        speaker = tts_settings["speaker"]
        # If no speaker specified but model has speakers, use default and warn
        if speaker is None and hasattr(coqui_tts, "speakers") and coqui_tts.speakers:
            default_speaker = coqui_tts.speakers[0]  # assuming the first is the default
            Logger.log_warning("AudioHelper", f"No speaker specified. Using default speaker: {default_speaker}")
            speaker = default_speaker
        
        kwargs = {
            "text"              : text,
            "speed"             : tts_settings["speed"],
            "energy"            : tts_settings["energy"],
            "speaker"           : speaker,
            "speaker_wav"       : tts_settings["speaker_wav"],
            "language"          : tts_settings["language"],
            "file_path"         : output_audio_path
        }
        
        Utils.ensure_dir(output_audio_path)
        
        coqui_tts.tts_to_file(**kwargs)
        
        return AudioHelper().load_audio(output_audio_path)
    