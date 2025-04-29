
from core.frameworks.base       import BaseHandler
from core.frameworks.moviepy    import MoviePyBuilder

class MoviePyHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.commands       = {
            "generate-video"        : self.generate_video,
            "combine-videos"        : self.combine_videos,
            "apply-text-overlay"    : self.apply_text_overlay,
            "apply-subtitle"        : self.apply_subtitle,
            "generate-subtitle"     : self.generate_subtitle
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

    def combine_videos(self, action):
        try:
            self.logger.info("[MoviePyHandler] Combining videos")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.merge_videos(action).save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in combine-videos: {e}")

    def apply_text_overlay(self, action):
        try:
            self.logger.info("[MoviePyHandler] Adding text overlay")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action)
            moviePyBuilder.insert_overlay(action).apply_overlays()
            moviePyBuilder.save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error adding text overlay: {e}")

    def apply_subtitle(self, action):
        try:
            self.logger.info("[MoviePyHandler] Adding subtitles")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action)
            moviePyBuilder.add_subtitles(action).apply_overlays()
            moviePyBuilder.save(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error adding subtitles: {e}")

    def generate_subtitle(self, action):
        try:
            self.logger.info("[MoviePyHandler] Generating subtitles from source.")
            
            moviePyBuilder = MoviePyBuilder()
            moviePyBuilder.load(action).generate_subtitle(action)
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error in generate-subtitle: {e}")
