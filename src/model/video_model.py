
# -----------------------------------------------------------------------------
# src/model/video_model.py
# -----------------------------------------------------------------------------

from src.core               import BaseNode, command, Console
from src.file               import TextFile
from src.file.backend       import MoviepyAudioFile, MoviepyImageFile, MoviepyVideoFile
from src.model              import BaseModel
from src.model.helper       import VideoHelper

# -----------------------------------------------------------------------------
# VideoModel
#
# * Gives access to all usable video commands
# * Has the ability to access the JSON configuration with convenient
# python functions and names
# -----------------------------------------------------------------------------


class VideoModel(BaseModel):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self):
        super().__init__()

    # -------------------------------------------------------------------------
    # Generation with AI models
    # -------------------------------------------------------------------------

    @command("text-to-video")
    def text_to_video(self, context: BaseNode) -> None:
        text_file = TextFile.from_source(
            context.input_text,
            context.input_text_path,
            context.input_text_reference
        )
        video = VideoHelper.from_text(
            text=text_file.text,
            duration=context.duration.get(0.1)
        )
        MoviepyVideoFile(video).to_destination(
            context.output_video_path,
            context.output_video_reference
        )

    @command("image-to-video")
    def image_to_video(self, context: BaseNode) -> None:
        image_file = MoviepyImageFile.from_source(
            context.input_image_path,
            context.input_image_reference
        )
        video = VideoHelper.from_image(
            image_file.image,
            duration=context.duration.get(0.1)
        )
        MoviepyVideoFile(video).to_destination(
            context.output_video_path,
            context.output_video_reference
        )

    # -------------------------------------------------------------------------
    # Video IO
    # -------------------------------------------------------------------------

    @command("import-as")
    def import_as(self, context : BaseNode) -> None:
        Console.info("Dummy implementation for 'import-as' command")

    @command("export-as")
    def export_as(self, context : BaseNode) -> None:
        Console.info("Dummy implementation for 'export-as' command")

    # -------------------------------------------------------------------------
    # General video transformations
    # -------------------------------------------------------------------------

    @command("merge-videos")
    def merge_videos(self, context: BaseNode) -> None:
        videos: list = []

        # Load audio from file paths
        if context.input_video_paths:
            for file_path in context.input_video_paths:
                videos.append(
                    MoviepyVideoFile.from_source(file_path, None).video
                )

        # Load audio from cache
        if context.input_video_references:
            for video_reference in context.input_video_references:
                videos.append(
                    MoviepyVideoFile.from_source(None, video_reference).video
                )

        if videos:
            video = VideoHelper.merge(videos)
            MoviepyVideoFile(video).to_destination(
                context.output_video_path,
                context.output_video_reference
            )
        else:
            Console.error("No valid video inputs for merge")

    @command("compose-videos")
    def compose_videos(self, context: BaseNode) -> None:
        videos: list = []

        # Load audio from file paths
        if input_video_paths:
            for file_path in context.input_video_paths:
                videos.append(
                    MoviepyVideoFile.from_source(file_path, None).video
                )

        # Load audio from cache
        if input_video_references:
            for video_reference in context.input_video_references:
                videos.append(
                    MoviepyVideoFile.from_source(None, video_reference).video
                )

        if videos:
            video = VideoHelper.compose(videos)
            MoviepyVideoFile(video).to_destination(
                context.output_video_path,
                context.output_video_reference
            )
        else:
            Console.error("No valid video inputs for compose")

    @command("with-audio")
    def with_audio(self, context: BaseNode) -> None:
        audio_file = MoviepyAudioFile.from_source(
            context.input_audio_path,
            context.input_audio_reference
        )

        video_file = MoviepyVideoFile.from_source(
            context.input_video_path,
            context.input_video_reference
        )
        video = VideoHelper.with_audio(
            video_file.video,
            audio_file.audio
        )
        MoviepyVideoFile(video).to_destination(
            context.output_video_path,
            context.output_video_reference
        )

    @command("set-video-opacity")
    def set_video_opacity(self, context: BaseNode) -> None:
        video_file = MoviepyVideoFile.from_source(
            context.input_video_path,
            context.input_video_reference
        )
        video = VideoHelper.with_opacity(
            video_file.video,
            context.opacity.get()
        )
        MoviepyVideoFile(video).to_destination(
            context.output_video_path,
            context.output_video_reference
        )

    @command("update-video-settings")
    def update_video_settings(self, context: BaseNode) -> None:
        Console.info(f"Dummy update-video-settings")

# -----------------------------------------------------------------------------
