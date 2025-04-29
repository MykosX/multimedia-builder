
import os

from moviepy.editor import concatenate_videoclips, ImageClip, AudioFileClip, VideoFileClip
from core.utils.utils import Utils
from core.utils.logger import SimpleLogger
from core.handlers.base_handler import BaseHandler


class MoviePyHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.codec = "libx264"
        self.fps = 60
        self.default_duration = 5.0

        self.commands = {
            "generate_video": self.generate_video,
            "add_blank_screen": self.add_blank_screen,
            "combine_videos": self.combine_videos
        }

    def load_defaults(self, defaults):
        self.codec = defaults.get("codec", self.codec)
        self.fps = defaults.get("fps", self.fps)
        self.default_duration = defaults.get("duration", self.default_duration)
        self.logger.info(f"[MoviePyHandler] Loaded defaults: codec={self.codec}, fps={self.fps}, duration={self.default_duration}")

    def generate_video(self, action):
        image_path = action.get("image")
        audio_path = action.get("audio")
        output_path = action.get("output")

        if not all([image_path, audio_path, output_path]):
            self.logger.warning("[MoviePyHandler] Missing parameters for video generation.")
            return

        try:
            image_clip = ImageClip(image_path).set_fps(self.fps)
            audio_clip = AudioFileClip(audio_path)
            image_clip = image_clip.set_duration(audio_clip.duration)
            video_clip = image_clip.set_audio(audio_clip)

            Utils.ensure_dir(os.path.dirname(output_path))
            video_clip.write_videofile(output_path, codec=self.codec, fps=self.fps)

            self.logger.info(f"[MoviePyHandler] Video created: {output_path}")
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error generating video: {e}")

    def add_blank_screen(self, action):
        duration = action.get("duration", self.default_duration)
        output_path = action.get("output")
        color = tuple(action.get("color", (0, 0, 0)))
        size = tuple(action.get("size", (1280, 720)))

        if not output_path:
            self.logger.warning("[MoviePyHandler] Output path required for blank screen.")
            return

        try:
            blank_clip = ImageClip(color=color, size=size).set_duration(duration).set_fps(self.fps)
            Utils.ensure_dir(os.path.dirname(output_path))
            blank_clip.write_videofile(output_path, codec=self.codec, fps=self.fps)
            self.logger.info(f"[MoviePyHandler] Blank screen video created: {output_path}")
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error creating blank screen: {e}")

    def combine_videos(self, action):
        video_paths = action.get("videos")
        output_path = action.get("output")

        if not video_paths or not output_path:
            self.logger.warning("[MoviePyHandler] Missing videos or output path for combination.")
            return

        try:
            clips = [VideoFileClip(path) for path in video_paths]
            final_clip = concatenate_videoclips(clips)
            Utils.ensure_dir(os.path.dirname(output_path))
            final_clip.write_videofile(output_path, codec=self.codec, fps=self.fps)
            self.logger.info(f"[MoviePyHandler] Combined video saved to: {output_path}")
        except Exception as e:
            self.logger.error(f"[MoviePyHandler] Error combining videos: {e}")
