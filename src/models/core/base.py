
from abc                import ABC, abstractmethod
from src.utils          import SimpleLogger, Utils

class BaseModel(ABC):
    cache = {}
    
    def __init__(self):
        self.logger         = SimpleLogger.get_logger()
        self.commands       = {}

    def log_info(self, prefix, msg):
        self.logger.info(f"[{prefix}] {msg}")

    def log_debug(self, prefix, msg):
        self.logger.debug(f"[{prefix}] {msg}")

    def log_warning(self, prefix, msg):
        self.logger.warning(f"[{prefix}] {msg}")

    def log_error(self, prefix, msg):
        self.logger.error(f"[{prefix}] {msg}")

    def load_from_cache(self, data_class, cache_key):
        name_key = f"{data_class}-{cache_key}"

        try:
            self.log_info("BaseModel", f"Loading {data_class.upper()} from cache as '{name_key}'")

            cache = self.__class__.cache
            if name_key in cache:
                return cache[name_key]
            else:
                self.log_warning("BaseModel", f"Cache key '{name_key}' not found.")

        except Exception as e:
            self.log_error("BaseModel", f"Error while loading {data_class.upper()} from cache as '{name_key}': {e}")

        return None
        
    def save_to_cache(self, data_class, cache_key, content):
        name_key = f"{data_class}-{cache_key}"

        try:
            self.log_info("BaseModel", f"Saving {data_class.upper()} to cache as '{name_key}'")

            cache = self.__class__.cache
            cache[name_key] = content
        except Exception as e:
            self.log_error("BaseModel", f"Error while saving {data_class.upper()} to cache as '{name_key}': {e}")

    def run(self, activity):
        self.log_debug("BaseModel", f"Running activity: {activity.get('name', 'Unnamed')}")

        for action in activity.get("actions", []):
            self.handle(action)

    def handle(self, action):
        command = action.get("command")
        enabled = action.get("enabled", True)
        if not enabled:
            self.log_warning("BaseModel", f"Action {command} is disabled. Skipping.")
            return

        if not command:
            self.log_warning("BaseModel", "No action specified in command.")
            return

        func = self.commands.get(command)
        if func:
            self.log_debug("BaseModel", f"Executing command: {command}")
            func(action)
        else:
            self.log_error("BaseModel", f"Unknown command: {command}")

