
# -----------------------------------------------------------------------------
# src/file/backend/moviepy_video_file.py
# -----------------------------------------------------------------------------

from typing                 import Self

from src.file               import VideoFile

from moviepy                import VideoFileClip

# -----------------------------------------------------------------------------
# MoviepyVideoFile
#
# * Wrapper for moviepy's video data (VideoFileClip)
# -----------------------------------------------------------------------------


class MoviepyVideoFile(VideoFile):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, video: VideoFileClip):
        super().__init__(video)

    # -------------------------------------------------------------------------
    # IO access to movie clips
    # -------------------------------------------------------------------------

    @classmethod
    def from_file(cls, source_path: str) -> Self:
        return cls(VideoFileClip(source_path))

    def to_file(self, destination_path: str) -> None:
        self.video.write_videofile(destination_path, fps=50)

# -----------------------------------------------------------------------------
