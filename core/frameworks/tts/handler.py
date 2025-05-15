
from core.frameworks.base   import BaseHandler
from core.frameworks.tts    import TTSBuilder
from TTS.api                import TTS

class TTSHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.tts            = None

        self.commands       = {
            "generate-speech"       : self.generate_speech,
            "create-silence"        : self.create_silence,
            "combine-audios"        : self.combine_audios,
            "generate-transcript"   : self.generate_transcript
        }

    def load_defaults(self, defaults):
        self.language       = defaults.get("language", "en")
        self.model_path     = defaults.get("model-path", "tts_models/en/ljspeech/vits")

        self.tts = TTS(self.model_path)
        self.logger.debug(f"[TTSHandler] Initialized TTS model: {self.model_path}")

    def generate_speech(self, action):
        try:
            self.logger.info("[TTSHandler] Generating speech")
            
            tts_builder = TTSBuilder()
            tts_builder.set_tts(self.tts).set_text(action)
            tts_builder.to_speech(action).save(action)
        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in generate-speech: {e}")

    def create_silence(self, action):
        try:
            self.logger.info("[TTSHandler] Creating silence")

            tts_builder = TTSBuilder()
            tts_builder.create_silence(action).save(action)
            
        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in create-silence: {e}")

    def combine_audios(self, action):
        try:
            self.logger.info(f"[TTSHandler] Starting combining audios.")

            tts_builder = TTSBuilder()
            tts_builder.combine_audios(action).save(action)
            
        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in combine-audios: {e}")

    def generate_transcript(self, action):
        try:
            self.logger.info(f"[TTSHandler] Generating transcript from audio")

            tts_builder = TTSBuilder()
            tts_builder.load(action).to_transcript(action)

        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in generate-transcript: {e}")