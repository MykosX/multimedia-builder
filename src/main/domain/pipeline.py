
# src/main/domain/pipeline.py

import json
import os
from src.utils                  import Logger, Utils

class Pipeline:
    def __init__(self, path, executor):
        self.path = path
        self.executor = executor

        self.title = None
        self.activities = []

    def load(self):
        if not os.path.exists(self.path):
            Logger.log_error("Pipeline", f"Pipeline not found: {self.path}")
            return False

        data = json.loads(Utils.load_text(self.path))

        self.title = data.get("subproject-title", "Unnamed Subproject")
        self.activities = data.get("activities", [])

        Logger.log_info("Pipeline", f"Loaded pipeline: {self.title}")
        return True

    def run(self):
        Logger.log_info("Pipeline", f"Running pipeline: {self.title}")

        for idx, activity in enumerate(self.activities):
            name = activity.get("name", f"Step {idx}")
            Logger.log_info("Pipeline", f"▶ Activity: {name}")

            self.executor.execute(activity)

            Logger.log_info("Pipeline", f"✔ Done: {name}")
