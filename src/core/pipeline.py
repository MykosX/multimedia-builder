
# -----------------------------------------------------------------------------
# src/core/pipeline.py
# -----------------------------------------------------------------------------

from src.core               import BaseNode, Config, Console, ModelRegistry
from src.file               import JsonFile

# -----------------------------------------------------------------------------
# Pipeline
#
# * Opens active pipelines
# * Handles activities and their corresponding actions
# -----------------------------------------------------------------------------


class Pipeline(Config):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self, config):
        super().__init__(config)

    @classmethod
    def load(cls, file_path : BaseNode):
        config = JsonFile.from_file(f"{file_path}").json
        return cls(config)

    # -------------------------------------------------------------------------
    # Run
    # -------------------------------------------------------------------------

    def run(self):
        Console.info(f"Pipeline: {self.config.project_title}")

        pipeline_defaults: BaseNode = self.config.defaults or BaseNode.create({})

        for activity in self.config.activities:
            if activity.enabled:
                Console.info(f"Activity: {activity.name}")

                activity_defaults = pipeline_defaults.clone()

                if activity.defaults:
                    activity_defaults.update(activity.defaults)

                for action in activity.actions:
                    if action.enabled:
                        context = activity_defaults.clone()
                        context.update(action)
        
                        ModelRegistry.run(
                            f"{activity.model}",
                            context
                        )
                    else:
                        Console.warning(f"Action '{action.command}' is disabled.")
            else:
                Console.warning(f"Activity '{activity.name}' is disabled.")

# -----------------------------------------------------------------------------
