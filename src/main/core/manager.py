
# src/main/core/manager.py

from src.main.core              import ActivityExecutor
from src.main.domain            import Workspace, Pipeline
from src.utils                  import Logger

class WorkspaceManager:
    def __init__(self):
        self.workspace = Workspace()
        self.executor = ActivityExecutor()

    def load_workspace(self, path):
        self.workspace.load(path)

    def run(self):
        Logger.log_info("WorkspaceManager", f"Project: {self.workspace.project_title}")

        for pipeline_info in self.workspace.get_enabled_pipelines():
            pipeline = Pipeline(
                path=pipeline_info["path"],
                executor=self.executor
            )

            if pipeline.load():
                pipeline.run()
