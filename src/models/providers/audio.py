
# src/models/providers/audio.py

from pydub                      import AudioSegment
from src.utils                  import Logger, Utils


class AudioHelper:
    def __init__(self, audio_segment=None):
        self.audio_segment = audio_segment or AudioSegment.silent(0)

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
