
# src/utils/logger.py

import os

from datetime                   import datetime
from colorama                   import Fore, Style, init as colorama_init

class Logger:
    INSTANCE = None

    # -------- singleton control --------
    def __new__(cls, log_dir="logs", log_file=None):
        if cls.INSTANCE is None:
            cls.INSTANCE = super().__new__(cls)
            cls.INSTANCE._init(log_dir, log_file)
        return cls.INSTANCE

    # -------- initialization done once --------
    def _init(self, log_dir, log_file):
        colorama_init(autoreset=True)
        os.makedirs(log_dir, exist_ok=True)

        if not log_file:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = f"{log_dir}/run_{now}.log"

        self.log_file_path = log_file
        
        self._log("INFO", f"[Logger] Logger initialized. Saving logs to {self.log_file_path}")
   

    # -------- intern helpers (private) --------
    def _write_file(self, message):
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(message + "\n")

    def _write_console(self, level, message):
        color_map = {
            "INFO": Fore.WHITE,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "DEBUG": Fore.CYAN
        }
        color = color_map.get(level, Fore.WHITE)
        print(f"{color}[{level}] {message}{Style.RESET_ALL}")

    def _log(self, level, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"{timestamp} - [{level}] {message}"
        self._write_console(level, message)
        self._write_file(line)

    # -------- public API --------
    @classmethod
    def log_info(cls, prefix, message):
        cls()._log("INFO", f"[{prefix}] {message}")

    @classmethod
    def log_warning(cls, prefix, message):
        cls()._log("WARNING", f"[{prefix}] {message}")

    @classmethod
    def log_error(cls, prefix, message):
        cls()._log("ERROR", f"[{prefix}] {message}")

    @classmethod
    def log_debug(cls, prefix, message):
        cls()._log("DEBUG", f"[{prefix}] {message}")

