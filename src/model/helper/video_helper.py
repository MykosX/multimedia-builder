
# -----------------------------------------------------------------------------
# src/model/helper/video_helper.
# # -----------------------------------------------------------------------------

from typing                 import Self

from src.core               import Logger

from moviepy                import AudioClip, concatenate_videoclips, CompositeVideoClip, ImageClip, TextClip, VideoClip

# -----------------------------------------------------------------------------
# VideoHelper
#
# * Gives access to specific video IO functions
# * Provides access to video transformations
# -----------------------------------------------------------------------------


class VideoHelper:
    # -------------------------------------------------------------------------
    # Video IO
    # -------------------------------------------------------------------------

    def import_as(self) -> VideoHelper:
        pass

    def export_as(self) -> None:
        pass

    # -------------------------------------------------------------------------
    # General video transformations
    # -------------------------------------------------------------------------

    @classmethod
    def from_text(cls, text: str, font_size: int = 40, duration: float = 0.1) -> TextClip:
        return TextClip(text=text, font_size=font_size).with_duration(duration)

    @classmethod
    def from_image(cls, image_clip: ImageClip, duration: float = 0.1) -> ImageClip:
        return image_clip.with_duration(duration)

    @classmethod
    def with_audio(cls, video: VideoClip, audio_clip: AudioClip) -> VideoClip:
        return video.with_duration(audio_clip.duration).with_audio(audio_clip)

    @classmethod
    def merge(cls, videos: list[VideoClip]) -> VideoClip:
        return concatenate_videoclips(videos)

    @classmethod
    def compose(cls, videos: list[VideoClip]) -> VideoClip:
        return CompositeVideoClip(videos)

    @classmethod
    def split(cls, video:VideoClip, split_times: Iterable[float] = [1.0, 2.0]) -> list[VideoClip]:
        video_length_sec = len(video) / 1000.0

        # Filter valid split times
        valid_split_times = []
        for split_time in sorted(split_times):
            if 0 < split_time < video_length_sec:
                valid_split_times.append(split_time)
            else:
                Logger.warning(
                    type(self),
                    f"Ignoring out-of-range split time: {split_time}"
                )

        # Always include the end of the video.
        valid_split_times.append(video_length_sec)

        Logger.info(
            type(self),
            f"Splitting video at: {valid_split_times}"
        )

        clips: list[VideoClip] = []
        start_ms = 0
        
        for split_time in valid_split_times:
            end_ms = int(split_time * 1000)
            clips.append(video.subclipped(start_ms, end_ms))
            start_ms = end_ms
        
        return clips

    @classmethod
    def resize(cls, video: VideoClip, width: int, height: int) -> VideoClip:
        return video.resize((width, height))

    @classmethod
    def with_time(cls, video: VideoClip, start: float | None = None, duration: float | None = None) -> VideoClip:
        if start is not None:
            video = video.with_start(start)

        if duration is not None:
            video = video.with_duration(duration)

        return video

    @classmethod
    def with_position(cls, video: VideoClip, x: int | str = 0, y: int | str = 0) -> VideoClip:
        return video.with_position((x, y))

    @classmethod
    def with_opacity(cls, video: VideoClip, opacity: float = 1.00) -> VideoClip:
        return video.with_opacity(opacity)

# -----------------------------------------------------------------------------
