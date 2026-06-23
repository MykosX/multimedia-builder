
# -----------------------------------------------------------------------------
# src/file/backend/pillow_image_file.py
# -----------------------------------------------------------------------------

from typing                 import Self

from src.file               import ImageFile

from PIL                    import Image

# -----------------------------------------------------------------------------
# PillowImageFile
#
# * Wrapper for pillow's image data (Image)
# -----------------------------------------------------------------------------


class PillowImageFile(ImageFile):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, image: Image  = None):
        super().__init__(image)

    # -------------------------------------------------------------------------
    # IO access to pillow images
    # -------------------------------------------------------------------------

    @classmethod
    def from_file(cls, source_path: str) -> Self:
        return cls(Image.open(source_path))

    def to_file(self, destination_path: str) -> None:
        self.image.save(destination_path)

# -----------------------------------------------------------------------------
