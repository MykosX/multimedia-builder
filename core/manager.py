
import json
import os

from core.handlers.tts_handler import TTSHandler
from core.handlers.sdp_handler import SDPHandler
from core.handlers.moviepy_handler import MoviePyHandler
from core.utils.logger import SimpleLogger

class ProjectManager:
    def __init__(self):
        self.logger = SimpleLogger.get_logger()
        self.handlers = {
            "tts": TTSHandler,
            "sdp": SDPHandler,
            "moviepy": MoviePyHandler
        }

    def load_manager_json(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.manager_json = json.load(f)

    def run(self):
        project_title = self.manager_json.get("project_title", "Unnamed Project")
        self.logger.info(f"📁 Starting project: {project_title}\n")
        
        pipelines = self.manager_json.get("pipelines", [])
        for pipeline in pipelines:
            if pipeline.get("enabled", True):
                self.run_pipeline(pipeline['path'])
            else:
                self.logger.warning(f"❌ Skipping disabled pipeline: {pipeline['path']}\n")

    def run_pipeline(self, pipeline_path):
        self.logger.debug(f"🛠️  Loading subproject: {pipeline_path}\n")
        if not os.path.exists(pipeline_path):
            self.logger.error(f"❗ Cannot find pipeline file: {pipeline_path}\n")
            return

        with open(pipeline_path, 'r', encoding='utf-8') as f:
            pipeline_json = json.load(f)

        subproject_title = pipeline_json.get("subproject_title", "Unnamed Subproject")
        self.logger.info(f"➡️ Running subproject: {subproject_title}\n")

        activities = pipeline_json.get("activities", [])
        for idx, activity in enumerate(activities):
            step_name = activity.get("name", f"Step {idx}")
            self.logger.info(f"\n▶️ Starting activity: {step_name}\n")
            
            type_ = activity.get("type")
            handler_class = self.handlers.get(type_)

            if not handler_class:
                self.logger.error(f"❌ Unknown handler type: {type_}\n")
                continue

            try:
                handler = handler_class()
                handler.run(activity)
                self.logger.info(f"✅ Completed activity: {step_name}\n")

            except Exception as e:
                self.logger.error(f"❗ Error in activity {step_name}: {e}\n")
