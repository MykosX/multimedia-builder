import os
from TTS.api import TTS
from core.utils.utils import Utils
from core.handlers.base_handler import BaseHandler

class TTSHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.tts = None
        self.commands = {
            "generate_speech": self.generate_speech,
            "add_silence": self.add_silence  # stub
        }

    def load_defaults(self, defaults):
        self.language = defaults.get("language", "en")
        self.model_path = defaults.get("model_path", "tts_models/en/ljspeech/vits")
        self.speed = defaults.get("speed", 1.0)
        self.energy = defaults.get("energy", 1.0)
        self.speaker = defaults.get("speaker", "default")

        self.tts = TTS(self.model_path)
        self.logger.debug(f"[TTSHandler] Initialized TTS model: {self.model_path}")

    def generate_speech(self, action):
        text = action.get("text")
        text_source = action.get("text_source")
        output_path = action.get("output")

        if text_source and os.path.isfile(text_source):
            with open(text_source, "r", encoding="utf-8") as f:
                text = f.read().strip()

        if not text:
            self.logger.warning("No text found for generate_speech.")
            return

        Utils.ensure_dir(os.path.dirname(output_path))

        kwargs = {
            "text": text,
            "file_path": output_path,
            "speed": self.speed,
            "energy": self.energy,
            "speaker": self.speaker
        }

        self.logger.info(f"[TTSHandler] Generating speech to: {output_path}")
        self.tts.tts_to_file(**kwargs)

    def add_silence(self, action):
        duration = action.get("duration", 1.0)
        output_path = action.get("output")

        self.logger.info(f"[TTSHandler] Adding silence ({duration}s) to: {output_path}")
        # TODO: implement AudioUtils.add_silence(duration, output_path)
