
import json
from src.utils          import Utils


class Workspace:
    def __init__(self, logger):
        self.logger = logger
        self.project_title = None
        self.pipelines = []

    def load(self, filepath):
        data = json.loads(Utils.load_text(filepath))

        self.project_title = data.get("project-title", "Unnamed Project")
        self.pipelines = data.get("pipelines", [])

        self.logger.info(f"Loaded workspace: {self.project_title}")

    def get_enabled_pipelines(self):
        return [
            p for p in self.pipelines
            if p.get("enabled", True)
        ]
