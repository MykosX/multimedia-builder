
import pysrt
import whisper

from core.frameworks.base   import BaseBuilder
from core.utils             import Utils
from moviepy.editor         import AudioFileClip, concatenate_videoclips, ColorClip, CompositeVideoClip, ImageClip, VideoFileClip, TextClip
from PIL                    import ImageColor

class MoviePyBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.codec          = "libx264"
        self.fps            = 50
        self.video          = None
        self.overlays       = []

    def load_audio(self, source_path):
        try:
            self.logger.info(f"[MoviePyBuilder] Loading audio from: {source_path}")
            
            return AudioFileClip(source_path)
        except Exception as e:
            self.logger.error(f"[MoviePyBuilder] Error while loading audio: {e}")
            return None

    def save_audio(self, audio, destination_path):
        try:
            self.logger.info(f"[MoviePyBuilder] Saving audio to: {destination_path}")
            
            Utils.ensure_dir(destination_path)
            audio.write_audiofile(destination_path)
        except Exception as e:
            self.logger.error(f"[MoviePyBuilder] Error while saving audio: {e}")

    def load_image(self, source_path):
        try:
            self.logger.info(f"[MoviePyBuilder] Loading image from: {source_path}")
            
            return ImageClip(source_path)
        except Exception as e:
            self.logger.error(f"[MoviePyBuilder] Error while loading image: {e}")
            return None

    def save_image(self, image, destination_path):
        try:
            self.logger.info(f"[MoviePyBuilder] Saving image to: {destination_path}")
            
            Utils.ensure_dir(destination_path)
            image.save_frame(destination_path)
        except Exception as e:
            self.logger.error(f"[MoviePyBuilder] Error while saving image: {e}")

    def load_video(self, source_path):
        try:
            self.logger.info(f"[MoviePyBuilder] Loading video from: {source_path}")
            
            return VideoFileClip(source_path)
        except Exception as e:
            self.logger.error(f"[MoviePyBuilder] Error while loading video: {e}")
            return None

    def save_video(self, video, destination_path):
        try:
            self.logger.info(f"[MoviePyBuilder] Saving video to: {destination_path}")
            
            Utils.ensure_dir(destination_path)
            video.write_videofile(destination_path, codec=self.codec, fps=self.fps)
        except Exception as e:
            self.logger.error(f"[MoviePyBuilder] Error while saving video: {e}")

    def load(self, action) -> 'MoviePyBuilder':
        """Load video from a given file or from cache."""
        input_video_path    = action.get("input-video-path")
        video_name          = action.get("video-name")

        if input_video_path:
            self.video = self.load_video(input_video_path)
        elif video_name:
            self.video = self.load_from_cache("video", video_name)
        else:
            self.logger.error("[MoviePyBuilder] No load source specified (file or cache).")
            
        return self

    def save(self, action) -> 'MoviePyBuilder':
        """Save video to cache or to a given file."""
        video_name          = action.get("video-name")
        output_video_path   = action.get("output-video-path")

        if not (output_video_path or video_name):
            self.logger.error("[MoviePyBuilder] No save target specified (file or cache).")
            
        if output_video_path:
            self.save_video(self.video, output_video_path)

        if video_name:
            self.save_to_cache("video", video_name, self.video)
        return self

    def generate_video(self, action) -> 'MoviePyBuilder':
        """Generate a video by combining provided image and audio."""
        input_image_path    = action.get("input-image-path")
        input_audio_path    = action.get("input-audio-path")

        image = self.load_image(input_image_path)
        audio = self.load_audio(input_audio_path)
        
        image.set_fps(self.fps).set_duration(audio.duration)
        self.video = image.set_audio(audio).set_duration(audio.duration)
            
        return self

    def merge_videos(self, action) -> 'MoviePyBuilder':
        """Merge video clips from file paths or cache keys into one video."""
        video_paths         = action.get("input-video-paths")
        video_names         = action.get("video-names")

        clips = []

        # Load audio from file paths
        if video_paths:
            for file_path in video_paths:
                clip = self.load_video(file_path)
                if clip:
                    clips.append(clip)

        # Load audio from cache
        if video_names:
            for video_name in video_names:
                clip = self.load_from_cache("video", video_name)
                if clip:
                    clips.append(clip)

        if not clips:
            self.logger.error("[TTSBuilder] No valid video clips found to merge.")
            return self

        self.video = concatenate_videoclips(clips, method="compose")
        return self

    def generate_subtitles(self, action) -> 'MoviePyBuilder':
        """Use Whisper to transcribe embedded audio with phrase timestamps."""
        subtitle_output_path= action.get("output-text-path")

        temp_file = subtitle_output_path+".wav"
        self.save_audio(self.video.audio, temp_file)
        
        # Use Whisper to generate subtitles
        model = whisper.load_model("base")
        result = model.transcribe(temp_file)

        # This is the list of subtitles with timestamps
        subs = result['segments']

        # Save subtitles in .srt format
        subtitle_text = ""
        for i, segment in enumerate(subs, 1):
            start_time  = Utils.format_time(segment['start'])
            end_time    = Utils.format_time(segment['end'])
            text = segment['text']
            subtitle_text += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
        
        #Delete temporary file
        Utils.delete_file(temp_file)
        #Now save the transcript
        self.save_text(subtitle_text, subtitle_output_path)
            
        return self

    @staticmethod
    def parse_color(value, default="black"):
        """
        Parses a color input (name, hex, RGB tuple). Returns (R, G, B).
        Falls back to `default` if parsing fails.
        """
        try:
            if isinstance(value, (tuple, list)) and len(value) == 3:
                return tuple(value)

            if isinstance(value, str):
                return ImageColor.getrgb(value.strip())

            return ImageColor.getrgb(default)
        except Exception:
            return (0, 0, 0)

    def subrip_to_seconds(self, subrip_time):
        return (
            subrip_time.hours * 3600 +
            subrip_time.minutes * 60 +
            subrip_time.seconds +
            subrip_time.milliseconds / 1000.0
        )
    
    def create_text_overlay(self, action) -> 'MoviePyBuilder':
        """Creates a text overlay."""
        font                = action.get("font", "Arial")
        font_size           = action.get("font-size", 32)
        color               = action.get("color", "white")
        text_position       = action.get("position", ("center", "center"))
        duration            = action.get("duration", 1.0)
        start_time          = action.get("start-time", 0.0)
        stop_time           = action.get("stop-time", 1.0)

        text = self.set_text(action)

        if not text:
            self.logger.error("[MoviePyBuilder] Cannot create text clip: no text set.")
            return self

        if not duration:
            duration = stop_time - start_time
        else:
            start_time = 0
        
        text_clip = TextClip(text, font=font, fontsize=font_size, color=color, method="label")
        text_clip = text_clip.set_position(text_position).set_duration(duration).set_start(start_time)

        self.video = text_clip
        return self
    
    def with_background(self, action) -> 'MoviePyBuilder':
        """Add background to existing video."""
        video_w, video_h = self.video.size
        
        background_color    = action.get("color", "black")
        background_opacity  = action.get("opacity", 0.5)
        width               = action.get("width")
        height              = action.get("height")

        current_clip = self.video
        if not (width and height):
            size = current_clip.size
        else:
            size = (width, height)
        rgb = self.parse_color(background_color)

        color_clip = ColorClip(size=size, color=rgb).set_opacity(background_opacity).set_position(current_clip.position).set_duration(current_clip.duration).set_start(current_clip.start)

        self.video = CompositeVideoClip([color_clip, current_clip])
        return self
    
    def place_clip(self, action) -> 'MoviePyBuilder':
        """Position current clip."""
        x                   = action.get("x")
        y                   = action.get("y")
        start_time          = action.get("start-time", 0.0)
        stop_time           = action.get("stop-time", 1.0)

        current_clip = self.video
        duration = stop_time - start_time
        
        if not (x and y):
            position = ("center", "center")
        else:
            position = (x, y)

        current_clip = current_clip.set_position(position).set_duration(duration).set_start(start_time)

        self.video = current_clip
        return self

    def compose_clips(self, action) -> 'MoviePyBuilder':
        """Compose video clips from file paths or cache keys over one video."""
        video_paths         = action.get("input-video-paths")
        video_names         = action.get("video-names")

        clips = []

        # Load audio from file paths
        if video_paths:
            for file_path in video_paths:
                clip = self.load_video(file_path)
                if clip:
                    clips.append(clip)

        # Load audio from cache
        if video_names:
            for video_name in video_names:
                clip = self.load_from_cache("video", video_name)
                if clip:
                    clips.append(clip)

        if not clips:
            self.logger.error("[TTSBuilder] No valid video clips found to merge.")
            return self

        self.video = CompositeVideoClip([self.video] + clips)
        return self

    def insert_overlay(self, action) -> 'MoviePyBuilder':
        """Add the current overlay pair (text + background) to the list of overlays."""
        video_w, video_h = self.video.size
        
        font                = action.get("font", "Arial")
        font_size           = action.get("font-size", 32)
        color               = action.get("color", "white")
        text_position       = action.get("text-position", ("center", "center"))
        background_color    = action.get("background-color", "black")
        background_opacity  = action.get("background-opacity", 0.5)
        size_behavior       = action.get("size-behavior", "fit-text")
        width               = action.get("width", video_w)
        height              = action.get("height", video_h)
        x                   = action.get("x", 0)
        y                   = action.get("y", 0)
        start_time          = action.get("start-time", 0.0)
        stop_time           = action.get("stop-time", 1.0)

        text = self.get_text(action)

        if not text:
            self.logger.error("[MoviePyBuilder] Cannot create text clip: no text set.")
            return self

        duration = stop_time - start_time
        box_size = (width, height)
        
        text_clip = TextClip(text, font=font, fontsize=font_size, color=color, method="label")
        text_clip = text_clip.set_position(text_position).set_duration(duration).set_start(0)

        if size_behavior == "full":
            color_clip_size = box_size
            color_position  = ("center", "center")
        else:
            color_clip_size = text_clip.size
            color_position  = text_position

        rgb = self.parse_color(background_color)

        color_clip = ColorClip(size=color_clip_size, color=rgb).set_opacity(background_opacity).set_position(color_position).set_duration(duration).set_start(0)

        box = CompositeVideoClip([color_clip, text_clip], size=box_size)
        box = box.set_position((x, y)).set_duration(duration).set_start(start_time)

        self.overlays.append(box)
        return self

    def apply_overlays(self) -> 'MoviePyBuilder':
        """Applies the overlays to current video."""
        self.video = CompositeVideoClip([self.video] + self.overlays)
        
        return self

    def add_subtitles( self, action) -> 'MoviePyBuilder':
        """Applies subtitles to current video."""
        subtitle_path       = action.get("input-text-path")

        subs = pysrt.open(subtitle_path)

        for sub in subs:
            start_time = self.subrip_to_seconds(sub.start)
            stop_time = self.subrip_to_seconds(sub.end)
            
            action["text"] = sub.text
            action["start-time"] = start_time
            action["stop-time"] = stop_time

            self.insert_overlay(action)

        return self
