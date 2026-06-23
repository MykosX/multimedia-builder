
# -----------------------------------------------------------------------------
# src/model/adapter/coqui_adapter.py
# -----------------------------------------------------------------------------

from src.core               import Config, Logger
from src.file               import BaseFile, TextFile
from src.file.backend       import PydubAudioFile

from TTS.api                import TTS

# -----------------------------------------------------------------------------
# CoquiAdapter
#
# * Gives access to Coqui TTS engine
# -----------------------------------------------------------------------------


class CoquiAdapter(Config):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self):
        super().__init__(
            {
                "model-path"        : "tts_models/en/ljspeech/vits",
                "speaker"           : None,
                "language"          : None,
                "speaker_wav"       : None
            }
        )

    # -------------------------------------------------------------------------
    # Internal interfaces
    # -------------------------------------------------------------------------

    def coqui_tts(self) -> TTS:
        Logger.info(
            type(self),
            f"Loading Coqui TTS model: {self.config.model_path}"
        )
        return TTS(f"{self.config.model_path}")

    @staticmethod
    def default_speaker(coqui_tts: TTS):
        # If the model has speakers, use first speaker available
        if hasattr(coqui_tts, "speakers") and coqui_tts.speakers:
            return coqui_tts.speakers[0]

        return None

    # -------------------------------------------------------------------------
    # Interfaces available to other classes
    # -------------------------------------------------------------------------

    def text_to_speech(self) -> None:
        text_file = TextFile.from_source(
            self.config.input_text,
            self.config.input_text_path,
            self.config.input_text_reference
        )

        coqui_tts = self.coqui_tts()

        file_path = BaseFile.find_destination(
            self.config.output_audio_path,
            self.config.output_audio_reference
        )

        kwargs = {
            "text"          : text_file.text,
            "speaker"       : self.config.speaker.get(),
            "language"      : self.config.language.get(),
            "speaker_wav"   : self.config.speaker_wav.get(),
            "file_path"     : file_path
        }

        coqui_tts.tts_to_file(**kwargs)

        # read-write to be able to save in cache if needed
        PydubAudioFile.from_file(
            file_path
        ).to_destination(
            self.config.output_audio_path,
            self.config.output_audio_reference
        )

# -----------------------------------------------------------------------------
