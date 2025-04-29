
from abc            import ABC
from core.utils     import SimpleLogger

class BaseHandler(ABC):
    cache = {}

    def __init__(self):
        self.logger = SimpleLogger.get_logger()
        self.commands = {}
        self.defaults = {}
        
    def load_defaults(self, defaults):
        pass

    def run(self, activity):
        self.logger.debug(f"[BaseHandler][{self.__class__.__name__}] Running activity: {activity.get('name', 'Unnamed')}")
        self.defaults = activity.get("defaults", {})
        self.load_defaults(self.defaults)

        for action in activity.get("actions", []):
            self.handle(action)

    def handle(self, action):
        command = action.get("command")
        enabled = action.get("enabled", True)
        if not enabled:
            self.logger.warning(f"[BaseHandler]Action {command} is disabled. Skipping.")
            return

        if not command:
            self.logger.warning("[BaseHandler]No action specified in command.")
            return

        func = self.commands.get(command)
        if func:
            self.logger.debug(f"[BaseHandler][{self.__class__.__name__}] Executing command: {command}")
            func(action)
        else:
            self.logger.error(f"[BaseHandler]Unknown command: {command}")

