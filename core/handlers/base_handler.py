from abc import ABC, abstractmethod
from core.utils.logger import SimpleLogger

class BaseHandler(ABC):
    def __init__(self):
        self.logger = SimpleLogger.get_logger()
        self.commands = {}
        self.defaults = {}

    def run(self, activity):
        self.logger.debug(f"[{self.__class__.__name__}] Running activity: {activity.get('name', 'Unnamed')}")
        self.defaults = activity.get("defaults", {})
        self.load_defaults(self.defaults)

        for action in activity.get("actions", []):
            self.handle(action)

    def handle(self, action):
        command = action.get("command")
        if not command:
            self.logger.warning("No command specified in action.")
            return

        func = self.commands.get(command)
        if func:
            self.logger.debug(f"[{self.__class__.__name__}] Executing command: {command}")
            func(action)
        else:
            self.logger.error(f"Unknown command: {command}")

    @abstractmethod
    def load_defaults(self, defaults):
        pass
