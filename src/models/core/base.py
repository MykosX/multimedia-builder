
# src/models/core/base.py

from abc                        import ABC, abstractmethod
from src.models.core.decorators import command
from src.utils                  import Logger

class BaseModel(ABC):
    CACHE           = {}
    COMMANDS        = {}
    
    def __init_subclass__(cls):
        super().__init_subclass__()

        # Copiază comenzile moștenite
        cls.COMMANDS = dict(getattr(cls, "COMMANDS", {}))

        # Adaugă comenzile definite în clasa curentă
        for method in cls.__dict__.values():
            if hasattr(method, "_command_name"):
                cls.COMMANDS[method._command_name] = method.__name__

    @staticmethod
    def load_from_cache(data_class, cache_key):
        name_key = f"{data_class}-{cache_key}"

        try:
            Logger.log_info("BaseModel", f"Loading {data_class.upper()} from cache as '{name_key}'")

            cache = BaseModel.CACHE
            if name_key in cache:
                return cache[name_key]
            else:
                Logger.log_warning("BaseModel", f"Cache key '{name_key}' not found.")

        except Exception as e:
            Logger.log_error("BaseModel", f"Error while loading {data_class.upper()} from cache as '{name_key}': {e}")

        return None

    @staticmethod
    def save_to_cache(data_class, cache_key, content):
        name_key = f"{data_class}-{cache_key}"

        try:
            Logger.log_info("BaseModel", f"Saving {data_class.upper()} to cache as '{name_key}'")

            cache = BaseModel.CACHE
            cache[name_key] = content
        except Exception as e:
            Logger.log_error("BaseModel", f"Error while saving {data_class.upper()} to cache as '{name_key}': {e}")
    
    @command("run-custom")
    def run_custom(self, action):
        Logger.log_info("BaseModel", "Dummy implementation for 'run-custom' command")

    def run(self, activity):
        Logger.log_debug("BaseModel", f"Running activity: {activity.get('name', 'Unnamed')}")

        for action in activity.get("actions", []):
            self.handle(action)

    def handle(self, action):
        command = action.get("command")
        enabled = action.get("enabled", True)
        if not enabled:
            Logger.log_warning("BaseModel", f"Action {command} is disabled. Skipping.")
            return

        if not command:
            Logger.log_warning("BaseModel", "No action specified in command.")
            return

        method_name = self.COMMANDS.get(command)
        if method_name:
            Logger.log_debug("BaseModel", f"Executing command: {command}")
            getattr(self, method_name)(action)
        else:
            Logger.log_error("BaseModel", f"Unknown command: {command}")

