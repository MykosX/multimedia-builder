
# -----------------------------------------------------------------------------
# src/file/backend/__init__.py
# -----------------------------------------------------------------------------

from .moviepy_audio_file    import MoviepyAudioFile
from .moviepy_image_file    import MoviepyImageFile
from .moviepy_video_file    import MoviepyVideoFile
from .pillow_image_file     import PillowImageFile
from .pydub_audio_file      import PydubAudioFile

# -----------------------------------------------------------------------------
# Available core classes
# -----------------------------------------------------------------------------

__all__ = [
    "MoviepyAudioFile",
    "MoviepyImageFile",
    "MoviepyVideoFile",
    "PillowImageFile",
    "PydubAudioFile"
]

# -----------------------------------------------------------------------------
