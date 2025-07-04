
from abc            import ABC, abstractmethod
from core.utils     import SimpleLogger, Utils

class BaseBuilder(ABC):
    cache = {}
    
    def __init__(self):
        self.logger         = SimpleLogger.get_logger()

    @abstractmethod
    def load(self, action) -> 'BaseBuilder':
        """Load data from a given file or from cache."""
        pass

    @abstractmethod
    def save(self, action) -> 'BaseBuilder':
        """Save data to cache or to a given file."""
        pass

    def load_text(self, source_path: str) -> str:
        try:
            self.logger.info(f"[BaseBuilder] Loading text from: {source_path}")
            
            with open(source_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            self.logger.error(f"[BaseBuilder] Error while loading text from {source_path}: {e}")
            return None

    def save_text(self, content: str, destination_path: str) -> None:
        try:
            self.logger.info(f"[BaseBuilder] Saving text to: {destination_path}")
            
            Utils.ensure_dir(destination_path)
            with open(destination_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            self.logger.error(f"[BaseBuilder] Error while saving text to {destination_path}: {e}")

    def get_text(self, action, text_key="text", text_path_key="input-text-path"):
        """Gets text directly or read it from a file."""
        text                = action.get(text_key)
        input_text_path     = action.get(text_path_key)

        if text:
            text_data = text
        elif input_text_path:
            text_data = self.load_text(input_text_path)
        else:
            self.logger.warning(f"[BaseBuilder] No text source specified ('{text_key}' or '{text_path_key}').")
            text_data = None
            
        return text_data

    def load_from_cache(self, data_type, cache_key):
        name_key = f"{data_type}-{cache_key}"

        try:
            self.logger.info(f"[BaseBuilder] Loading {data_type.upper()} from cache as '{name_key}'")

            cache = self.__class__.cache
            if name_key in self.__class__.cache:
                return self.__class__.cache[name_key]
            else:
                self.logger.warning(f"[BaseBuilder] Cache key '{name_key}' not found.")
                return None
        except Exception as e:
            self.logger.error(f"[BaseBuilder] Error while loading {data_type.upper()} from cache as '{name_key}': {e}")
            return None
        
    def save_to_cache(self, data_type, cache_key, content):
        name_key = f"{data_type}-{cache_key}"

        try:
            self.logger.info(f"[BaseBuilder] Saving {data_type.upper()} to cache as '{name_key}'")

            cache = self.__class__.cache
            cache[name_key] = content
        except Exception as e:
            self.logger.error(f"[BaseBuilder] Error while saving {data_type.upper()} to cache as '{name_key}': {e}")
