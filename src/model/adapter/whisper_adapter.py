
# -----------------------------------------------------------------------------
# src/model/adapter/whisper_adapter.py
# -----------------------------------------------------------------------------

import whisper

from src.core               import Config, Console, Logger
from src.file               import BaseFile
from src.model.helper       import TextHelper


# -----------------------------------------------------------------------------
# WhisperAdapter
#
# * Gives access to whisper engine
# -----------------------------------------------------------------------------


class WhisperAdapter(Config):
    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    def __init__(self):
        super().__init__(
            {
                "model"             : "base",
                "mode"              : "words"
            }
        )

    @staticmethod
    def extract_words(result: list[dict]) -> list[dict]:
        items = []

        for segment in result["segments"]:
            for word in segment["words"]:
                items.append({
                    "text"      : word["word"].strip(),
                    "start_time": word["start"],
                    "end_time"  : word["end"]
                })

        return items

    @staticmethod
    def extract_sentences(result: list[dict]) -> list[dict]:
        items = []

        for segment in result["segments"]:
            items.append({
                "text"      : segment["text"].strip(),
                "start_time": segment["start"],
                "end_time"  : segment["end"]
            })

        return items

    def whisper_model(self) -> whisper:
        Logger.info(
            type(self),
            f"Initialized Whisper STT model: {self.config.model}"
        )
        return whisper.load_model(self.config.model.get())

    def transcribe(self, audio_path: str) -> list[dict]:
        model   = self.whisper_model()
        mode    = self.config.mode.get()

        result = model.transcribe(
            audio           = audio_path,
            word_timestamps = (mode == "words")
        )

        if mode == "sentences":
            return self.extract_sentences(result)

        if mode != "words":
            Console.warning(f"Unknown transcription mode '{mode}'. Falling back to 'words'.")

        return self.extract_words(result)

    def speech_to_text(self) -> None:
        audio_path = BaseFile.find_source(
            self.config.input_audio_path,
            self.config.input_audio_reference
        )

        (
            TextHelper.from_timestamped(
                self.transcribe(
                    audio_path
                )
            ).to_destination(
                self.config.output_text_path,
                self.config.output_text_reference
            )
        )

# -----------------------------------------------------------------------------
