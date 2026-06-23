
# src/models/providers/text.py

from src.utils                  import Logger, Utils

class TextHelper:
    # loads text from specified file path
    @staticmethod
    def load_text(source_path: str) -> str:
        try:
            Logger.log_info("TextHelper", f"Loading text from: {source_path}")
            
            with open(source_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            Logger.log_error("TextHelper", f"Error while loading text from {source_path}: {e}")
            return None

    # saves text to a specified file
    @staticmethod
    def save_text(text: str, destination_path: str):
        try:
            Logger.log_info("TextHelper", f"Saving text to: {destination_path}")
            
            Utils.ensure_dir(destination_path)        
            with open(destination_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            Logger.log_error("TextHelper", f"Error while saving text to {destination_path}: {e}")

