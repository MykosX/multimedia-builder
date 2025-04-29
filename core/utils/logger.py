
import os

from datetime import datetime
from colorama import Fore, Style, init as colorama_init

class SimpleLogger:
    _instance = None

    def __new__(cls, log_dir="logs", log_file=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger(log_dir, log_file)
        return cls._instance

    def _init_logger(self, log_dir, log_file):
        colorama_init(autoreset=True)
        os.makedirs(log_dir, exist_ok=True)

        if not log_file:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = f"{log_dir}/run_{now}.log"

        self.log_file_path = log_file
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(f"[INFO] Logger initialized. Saving logs to {self.log_file_path}\n")

        self._log_to_console("Logger initialized. Saving logs to " + self.log_file_path, "INFO")

    def _log_to_file(self, message):
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(message + "\n")

    def _log_to_console(self, message, level):
        color_map = {
            "INFO": Fore.WHITE,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "DEBUG": Fore.CYAN
        }
        color = color_map.get(level, Fore.WHITE)
        print(f"{color}[{level}] {message}{Style.RESET_ALL}")

    def _log(self, message, level):
        timestamped = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [{level}] {message}"
        self._log_to_console(message, level)
        self._log_to_file(timestamped)

    def info(self, message):
        self._log(message, "INFO")

    def warning(self, message):
        self._log(message, "WARNING")

    def error(self, message):
        self._log(message, "ERROR")

    def debug(self, message):
        self._log(message, "DEBUG")

    @classmethod
    def get_logger(cls):
        return cls()

