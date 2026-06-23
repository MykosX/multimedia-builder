
# src/main/domain/workspace.py

import json
from src.utils                  import Logger, Utils

class Workspace:
    def __init__(self):
        self.project_title = None
        self.pipelines = []

    def load(self, filepath):
        data = json.loads(Utils.load_text(filepath))

        self.project_title = data.get("project-title", "Unnamed Project")
        self.pipelines = data.get("pipelines", [])

        Logger.log_info("Workspace", f"Loaded workspace: {self.project_title}")

    def get_enabled_pipelines(self):
        return [
            p for p in self.pipelines
            if p.get("enabled", True)
        ]
