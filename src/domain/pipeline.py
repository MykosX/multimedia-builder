
import json
import os
from src.utils          import Utils


class Pipeline:
    def __init__(self, path, logger, executor):
        self.path = path
        self.logger = logger
        self.executor = executor

        self.title = None
        self.activities = []

    def load(self):
        if not os.path.exists(self.path):
            self.logger.error(f"Pipeline not found: {self.path}")
            return False

        data = json.loads(Utils.load_text(self.path))

        self.title = data.get("subproject-title", "Unnamed Subproject")
        self.activities = data.get("activities", [])

        self.logger.info(f"Loaded pipeline: {self.title}")
        return True

    def run(self):
        self.logger.info(f"Running pipeline: {self.title}")

        for idx, activity in enumerate(self.activities):
            name = activity.get("name", f"Step {idx}")
            self.logger.info(f"▶ Activity: {name}")

            self.executor.execute(activity)

            self.logger.info(f"✔ Done: {name}")
