
import os

class Utils:
    @staticmethod
    def ensure_dir(path):
        """Ensure a directory exists."""
        os.makedirs(os.path.dirname(path), exist_ok=True)

    @staticmethod
    def delete_file(path):
        """Delete a file if it exists."""
        if os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def load_text(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

    @staticmethod
    def save_text(text, path):
        Utils.ensure_dir(path)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    @staticmethod
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"