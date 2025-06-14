
from core.frameworks.base   import BaseHandler
from core.frameworks.tts    import TTSBuilder

class TTSHandler(BaseHandler):
    def __init__(self):
        super().__init__()

        self.commands       = {
            "audio-to-text"             : self.audio_to_text,
            "combine-audios"            : self.combine_audios,
            "create-silence"            : self.create_silence,
            "show-models"               : self.show_models,
            "show-speakers"             : self.show_speakers,
            "split-audio"               : self.split_audio,
            "text-to-speech"            : self.text_to_speech
        }

    def load_defaults(self, defaults):
        TTSBuilder.load_defaults(defaults)

        #self.logger.debug(f"[TTSHandler] Initialized default TTS model: {model_path}")

    # audio-to-text command:
    # - loads the specified audio
    # - generates and saves transcript
    def audio_to_text(self, action):
        try:
            self.logger.info(f"[TTSHandler] Generating transcript from audio")

            tts_builder = TTSBuilder()
            tts_builder.load(action).generate_transcript(action)

        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in audio-to-text: {e}")

    # combine-audios command:
    # - combines provided audios into one final audio
    # - saves the final audio
    def combine_audios(self, action):
        try:
            self.logger.info(f"[TTSHandler] Starting combining audios.")

            tts_builder = TTSBuilder()
            tts_builder.combine_audios(action).save(action)
            
        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in combine-audios: {e}")

    # create-silence command:
    # - creates a silenced audio
    # - saves the resulted audio
    def create_silence(self, action):
        try:
            self.logger.info("[TTSHandler] Creating silence")

            tts_builder = TTSBuilder()
            tts_builder.create_silence(action).save(action)
            
        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in create-silence: {e}")

    # show-models command:
    # - shows available TTS models
    def show_models(self, action):
        try:
            self.logger.info("[TTSHandler] Showing available TTS models")

            tts_builder = TTSBuilder()
            tts_builder.show_models(action)
            
        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in show-models: {e}")

    # show-speakers command:
    # - shows speakers for specific TTS model
    def show_speakers(self, action):
        try:
            self.logger.info("[TTSHandler] Showing available speakers for selected TTS model")

            tts_builder = TTSBuilder()
            tts_builder.show_speakers(action)
            
        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in show-speakers: {e}")

    # split-audio command:
    # - loads the target audio
    # - splits it in more audios
    def split_audio(self, action):
        try:
            self.logger.info("[TTSHandler] Splitting audio file")

            tts_builder = TTSBuilder()
            tts_builder.load(action).split_audio(action)
            
        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in split-audio: {e}")

    # text-to-speech command:
    # - generates speech
    # - saves the audio file
    def text_to_speech(self, action):
        try:
            self.logger.info("[TTSHandler] Generating speech from text")
            
            tts_builder = TTSBuilder()
            tts_builder.text_to_speech(action).save(action)
        except Exception as e:
            self.logger.error(f"[TTSHandler] Error in text-to-speech: {e}")
