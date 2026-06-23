
from src.utils          import SimpleLogger
from src.domain         import Workspace, Pipeline
from src.core           import ActivityExecutor


class WorkspaceManager:
    def __init__(self):
        self.logger = SimpleLogger.get_logger()

        self.workspace = Workspace(self.logger)
        self.executor = ActivityExecutor(self.logger)

    def load_workspace(self, path):
        self.workspace.load(path)

    def run(self):
        self.logger.info(f"Project: {self.workspace.project_title}")

        for pipeline_info in self.workspace.get_enabled_pipelines():
            pipeline = Pipeline(
                path=pipeline_info["path"],
                logger=self.logger,
                executor=self.executor
            )

            if pipeline.load():
                pipeline.run()
