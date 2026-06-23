
# -----------------------------------------------------------------------------
# src/file/backend/moviepy_image_file.py
# -----------------------------------------------------------------------------

from typing                 import Self

from src.file               import ImageFile

from moviepy                import ImageClip

# -----------------------------------------------------------------------------
# MoviepyImageFile
#
# * Wrapper for moviepy's image data (ImageClip)
# -----------------------------------------------------------------------------


class MoviepyImageFile(ImageFile):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, image: ImageClip = None):
        super().__init__(image)

    # -------------------------------------------------------------------------
    # IO access to image clips
    # -------------------------------------------------------------------------

    @classmethod
    def from_file(cls, source_path: str) -> Self:
        return cls(ImageClip(source_path))

    def to_file(self, destination_path: str) -> None:
        self.image.save_frame(destination_path)

# -----------------------------------------------------------------------------
