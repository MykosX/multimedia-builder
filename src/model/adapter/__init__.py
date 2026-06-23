
# -----------------------------------------------------------------------------
# src/model/adapter/__init__.py
# -----------------------------------------------------------------------------

from .coqui_adapter         import CoquiAdapter
from .diffusers_adapter     import DiffusersAdapter
from .whisper_adapter       import WhisperAdapter

# -----------------------------------------------------------------------------
# Available core classes
# -----------------------------------------------------------------------------

__all__ = [
    "CoquiAdapter",
    "DiffusersAdapter",
    "WhisperAdapter"
]

# -----------------------------------------------------------------------------
