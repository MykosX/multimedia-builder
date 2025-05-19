
from core.frameworks.base       import BaseHandler
from core.frameworks.moviepy    import MoviePyBuilder

class MoviePyHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.commands       = {
            "generate-video"        : self.generate_video,
            "merge-videos"          : self.merge_videos,
            "compose-clips"         : self.compose_clips,
            "apply-text-overlay"    : self.apply_text_overlay,
            "create-text-overlay"   : self.create_text_overlay,
            "with-background"       : self.with_background,
            "place-clip"            : self.place_clip,
            "apply-subtitles"       : self.apply_subtitles,
            "generate-subtitles"    : self.generate_subtitles
        }

    def load_defaults(self, defaults):
        self.codec          = defaults.get("codec", "libx264")
        self.fps            = defaults.get("fps", 60)

        self.logger.info(f"[MoviePyHandler] Loaded defaults: codec={self.codec}, fps={self.fps}")

    def generate_video(self, action):
        try:
            self.logger.info("[MoviePyHandler] Generating video")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.generate_video(action).save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in generate-video: {e}")

    def merge_videos(self, action):
        try:
            self.logger.info("[MoviePyHandler] Combining videos")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.merge_videos(action).save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in combine-videos: {e}")

    def compose_clips(self, action):
        try:
            self.logger.info("[MoviePyHandler] Composing clips over existing video")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action).compose_clips(action).save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in compose-clips: {e}")

    def create_text_overlay(self, action):
        try:
            self.logger.info("[MoviePyHandler] Creating text overlay")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action).create_text_overlay(action).save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in create-text-overlay: {e}")

    def with_background(self, action):
        try:
            self.logger.info("[MoviePyHandler] Applying background to existing video")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action).with_background(action).save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in with-background: {e}")

    def place_clip(self, action):
        try:
            self.logger.info("[MoviePyHandler] Placing the clip on canvas")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action).place_clip(action).save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in place-clip: {e}")

    def apply_text_overlay(self, action):
        try:
            self.logger.info("[MoviePyHandler] Adding text overlay")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action)
            moviePyBuilder.insert_overlay(action).apply_overlays()
            moviePyBuilder.save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in apply-textoverlay: {e}")

    def apply_subtitles(self, action):
        try:
            self.logger.info("[MoviePyHandler] Adding subtitles")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action)
            moviePyBuilder.add_subtitles(action).apply_overlays()
            moviePyBuilder.save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in apply-subtitless: {e}")

    def generate_subtitles(self, action):
        try:
            self.logger.info("[MoviePyHandler] Generating subtitles from source.")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action).generate_subtitles(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in generate-subtitles: {e}")
