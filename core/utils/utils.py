
import os

class Utils:
    @staticmethod
    def ensure_dir(path):
        """Ensure a directory exists."""
        if not os.path.exists(path):
            os.makedirs(path)
