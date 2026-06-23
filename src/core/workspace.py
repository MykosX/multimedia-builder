
# -----------------------------------------------------------------------------
# src/core/workspace.py
# -----------------------------------------------------------------------------

from src.core               import Console, Config, Pipeline
from src.file               import BaseFile, JsonFile

# -----------------------------------------------------------------------------
# Workspace
#
# * Opens the workspace
# * Handles active pipelines
# -----------------------------------------------------------------------------


class Workspace(Config):
    # -------------------------------------------------------------------------
    # Class properties
    # -------------------------------------------------------------------------
    CONFIG_PATH     = "config/workspace.json"

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, config):
        super().__init__(config)

    @classmethod
    def open(cls):
        config = JsonFile.from_file(Workspace.CONFIG_PATH).json
        return cls(config)

    # -------------------------------------------------------------------------
    # Run
    # -------------------------------------------------------------------------

    def run(self):
        BaseFile.cache_cleanup()
        Console.info(f"Workspace: {self.config.workspace_title}")

        for pipeline in self.config.pipelines:
            if not pipeline.enabled:
                continue

            Pipeline.load(pipeline.path).run()

        BaseFile.cache_cleanup()

# -----------------------------------------------------------------------------
