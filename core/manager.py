
import json
import os

from core.frameworks.tts        import TTSHandler
from core.frameworks.sdp        import SDPHandler
from core.frameworks.gtrans     import GTransHandler
from core.frameworks.moviepy    import MoviePyHandler
from core.utils                 import SimpleLogger, Utils

class ProjectManager:
    def __init__(self):
        self.logger = SimpleLogger.get_logger()
        self.handlers = {
            "tts"       : TTSHandler,
            "sdp"       : SDPHandler,
            "gtrans"    : GTransHandler,
            "moviepy"   : MoviePyHandler
        }

    def load_manager_json(self, filepath):
        f = Utils.load_text(filepath)
        self.manager_json = json.loads(f)

    def run(self):
        project_title = self.manager_json.get("project-title", "Unnamed Project")
        self.logger.info(f"📁 Starting project: {project_title}")
        
        pipelines = self.manager_json.get("pipelines", [])
        for pipeline in pipelines:
            if pipeline.get("enabled", True):
                self.run_pipeline(pipeline['path'])
            else:
                self.logger.warning(f"❌ Skipping disabled pipeline: {pipeline['path']}")

    def run_pipeline(self, pipeline_path):
        self.logger.debug(f"🛠️  Loading subproject: {pipeline_path}")
        if not os.path.exists(pipeline_path):
            self.logger.error(f"❗ Cannot find pipeline file: {pipeline_path}")
            return

        f = Utils.load_text(pipeline_path)
        pipeline_json = json.loads(f)

        subproject_title = pipeline_json.get("subproject-title", "Unnamed Subproject")
        self.logger.info(f"➡️ Running subproject: {subproject_title}")

        activities = pipeline_json.get("activities", [])
        for idx, activity in enumerate(activities):
            step_name = activity.get("name", f"Step {idx}")
            self.logger.info(f"▶️ Starting activity: {step_name}")
            
            type_ = activity.get("type")
            handler_class = self.handlers.get(type_)

            if not handler_class:
                self.logger.error(f"❌ Unknown handler type: {type_}")
                continue

            try:
                handler = handler_class()
                handler.run(activity)
                self.logger.info(f"✅ Completed activity: {step_name}")

            except Exception as e:
                self.logger.error(f"❗ Error in activity {step_name}: {e}")
