
# -----------------------------------------------------------------------------
# src/model/audio_model.py
# -----------------------------------------------------------------------------

from pathlib                import Path

from src.core               import BaseNode, command, Console, Logger
from src.file.backend       import PydubAudioFile
from src.model              import BaseModel
from src.model.adapter      import CoquiAdapter, WhisperAdapter
from src.model.helper       import AudioHelper

# -----------------------------------------------------------------------------
# AudioModel
#
# * Gives access to all usable audio commands
# * Has the ability to access the JSON configuration with convenient
# python functions and names
# -----------------------------------------------------------------------------


class AudioModel(BaseModel):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self):
        super().__init__()

    # -------------------------------------------------------------------------
    # Generation with AI models
    # -------------------------------------------------------------------------

    @command("generate-speech-from-text")
    def generate_speech_from_text(self, context : BaseNode) -> None:
        Logger.debug(
            type(self),
            f"generate-speech-from-text: adapter={context.adapter}, parameters={context.parameters.get()}"
        )

        if context.adapter == "coqui":(
            CoquiAdapter()
            .update(context.parameters)
            .text_to_speech()
        )

    @command("generate-transcript-from-speech")
    def generate_transcript_from_speech(self, context) -> None:
        Logger.debug(
            type(self),
            f"generate-transcript-from-speech: adapter={context.adapter}, parameters={context.parameters.get()}"
        )

        if context.adapter == "whisper":(
            WhisperAdapter()
            .update(context.parameters)
            .speech_to_text()
        )

    # -------------------------------------------------------------------------
    # Audio IO
    # -------------------------------------------------------------------------

    @command("import-as")
    def import_as(self, context : BaseNode) -> None:
        Console.info("Dummy implementation for 'import-as' command")

    @command("export-as")
    def export_as(self, context : BaseNode) -> None:
        Console.info("Dummy implementation for 'export-as' command")

    # -------------------------------------------------------------------------
    # General audio transformations
    # -------------------------------------------------------------------------

    @command("merge-audios")
    def merge_audios(self, context : BaseNode) -> None:
        audio_segments: list = []

        # Load audio from file paths
        if context.input_audio_paths:
            for file_path in context.input_audio_paths:
                audio_segments.append(
                    PydubAudioFile.from_file(f"{file_path}").audio
                )

        # Load audio from cache
        if context.input_audio_references:
            for audio_reference in context.input_audio_references:
                audio_segments.append(
                    PydubAudioFile.from_cache(f"{audio_reference}").audio
                )

        if audio_segments:(
            PydubAudioFile(
                AudioHelper.merge(audio_segments)
            ).to_destination(
                context.output_audio_path,
                context.output_audio_reference
            )
        )
        else:
            Console.error("No valid audio inputs to merge")

    @command("with-silence")
    def with_silence(self, context : BaseNode) -> None:
        audio_file = PydubAudioFile.from_source(
            context.input_audio_path,
            context.input_audio_reference
        )

        # or just create silence
        (
            PydubAudioFile(
                AudioHelper.with_silence(
                    audio_file.audio,
                    context.duration.get()
                )
            ).to_destination(
                context.output_audio_path,
                context.output_audio_reference
            )
        )

    @command("split-audio")
    def split_audio(self, context : BaseNode) -> None:
        audio_file = PydubAudioFile.from_source(
            context.input_audio_path,
            context.input_audio_reference
        )
        chunks = AudioHelper.split(
            audio_file.audio,
            context.split_times.get()
        )

        p = Path(f"{context.output_audio_path}")
        for index, chunk in enumerate(chunks, start=1):
            part_path = p.parent / f"{p.stem}-part{index}{p.suffix}"
            chunk.to_file(BaseNode.create(part_path))

    # -------------------------------------------------------------------------
    # Custom commands
    # -------------------------------------------------------------------------

    @command("run-custom")
    def run_custom(self, context : BaseNode) -> None:
        Console.info("Dummy implementation for 'run-custom' command")

# -----------------------------------------------------------------------------
