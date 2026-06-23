
# -----------------------------------------------------------------------------
# src/file/backend/moviepy_audio_file.py
# -----------------------------------------------------------------------------

from typing                 import Self

from src.file               import AudioFile

from moviepy                import AudioFileClip

# -----------------------------------------------------------------------------
# MoviepyAudioFile
#
# * Wrapper for moviepy's audio data (AudioFileClip)
# -----------------------------------------------------------------------------


class MoviepyAudioFile(AudioFile):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, audio: AudioFileClip = None):
        super().__init__(audio)

    # -------------------------------------------------------------------------
    # IO access to audio clips
    # -------------------------------------------------------------------------

    @classmethod
    def from_file(cls, source_path: str) -> Self:
        return cls(AudioFileClip(source_path))

    def to_file(self, destination_path: str) -> None:
        self.resource.write_audiofile(destination_path)

# -----------------------------------------------------------------------------
