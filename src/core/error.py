
# -----------------------------------------------------------------------------
# src/core/error.py
# -----------------------------------------------------------------------------

from pathlib                import Path
import traceback

# -----------------------------------------------------------------------------
# Error
#
# * Exposes useful data about python exceptions
# -----------------------------------------------------------------------------


class Error:
    # -------------------------------------------------------------------------
    # Class properties
    # -------------------------------------------------------------------------

    PROJECT_ROOT = Path.cwd()

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, exception: Exception):
        self.exception = exception
        self.frame = traceback.extract_tb(exception.__traceback__)[-1]

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def file(self):
        try:
            return Path(self.frame.filename).resolve().relative_to(self.PROJECT_ROOT)
        except ValueError:
            return Path(self.frame.filename).name

    @property
    def line(self):
        return self.frame.lineno

    @property
    def function(self):
        return self.frame.name

    @property
    def message(self):
        return str(self.exception)

    # -------------------------------------------------------------------------
    # String
    # -------------------------------------------------------------------------

    def __str__(self):
        return f"{self.file}:{self.line}: {self.message}"

    def __repr__(self):
        return str(self)

# -----------------------------------------------------------------------------
