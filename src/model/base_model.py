
# -----------------------------------------------------------------------------
# src/model/base_model.py
# -----------------------------------------------------------------------------

from abc                    import ABC

from src.core               import BaseNode, Console, Error, Logger

# -----------------------------------------------------------------------------
# BaseModel
#
# * Creates the registry of supported commands
# * Runs a specific command
# -----------------------------------------------------------------------------


class BaseModel(ABC):
    # -------------------------------------------------------------------------
    # Class properties
    # -------------------------------------------------------------------------
    COMMANDS        = {}

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init_subclass__(cls):
        super().__init_subclass__()

        cls.COMMANDS = dict(getattr(cls, "COMMANDS", {}))

        for method in cls.__dict__.values():
            if hasattr(method, "_command_name"):
                command = method._command_name

                if command in cls.COMMANDS:
                    Logger.warning(
                        cls,
                        f"Overriding command '{command}'"
                    )

                cls.COMMANDS[command] = method

    # -------------------------------------------------------------------------
    # Run
    # -------------------------------------------------------------------------

    def run(self, context : BaseNode):
        command = context.command

        try:
            Console.info(f"Executing {command.json_name}:'{command}'")

            if command:
                method = self.COMMANDS.get(f"{command}")

                if method:
                        method(self, context)
                else:
                    raise Exception(f"{command.json_name} not implemented")
            else:
                raise Exception(f"Missing command")
        except Exception as e:
            Console.error(f"{command.json_name}:'{command}' execution failed: {Error(e)}")

# -----------------------------------------------------------------------------
