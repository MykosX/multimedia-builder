
# -----------------------------------------------------------------------------
# src/file/backend/pydub_audio_file.py
# -----------------------------------------------------------------------------

from typing                 import Self

from src.file               import AudioFile

from pydub                  import AudioSegment

# -----------------------------------------------------------------------------
# PydubAudioFile
#
# * Wrapper for pydub's audio data (AudioSegment)
# -----------------------------------------------------------------------------


class PydubAudioFile(AudioFile):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, audio: AudioSegment = None):
        super().__init__(audio)

    # -------------------------------------------------------------------------
    # IO access to audio segments
    # -------------------------------------------------------------------------

    @classmethod
    def from_file(cls, source_path: str) -> Self:
        return cls(AudioSegment.from_file(source_path))

    def to_file(self, destination_path: str) -> None:
        self.audio.export(destination_path)

# -----------------------------------------------------------------------------
