
# src/models/providers/coqui_tts.py

from src.models.domain          import AudioModel
from src.helpers.core           import Utils

from TTS.api                    import TTS

class CoquiTTS:
    def __init__(self):
        super().__init__()
        
        CoquiTTSModel.tts      = TTS("tts_models/multilingual/multi-dataset/your_tts")

    # Resolves and returns TTS model along with speech synthesis settings:
    # - initializes a new TTS model if 'model-path' is provided in action
    # - otherwise uses the class's default TTS model
    # - extracts and returns speech parameters like speed, energy, speaker, and speaker embeddings
    # - returns all as a dictionary for convenient access
    def resolve_model_settings(self, action):
        model_path          = action.get("model-path", None)
        speed               = action.get("speech-speed", 1.0)
        energy              = action.get("speech-energy", 1.0)
        speaker             = action.get("speech-speaker", None)
        speaker_wav         = action.get("input-voice-path", None)
        language            = action.get("language", None)

        if model_path:
            CoquiTTSModel.log_debug("CoquiTTSModel", f"Initialized object's TTS model: {model_path}")
            tts = TTS(model_path)
        else:
            tts = CoquiTTSModel.tts

        # If no speaker specified but model has speakers, use default and warn
        if speaker is None and hasattr(tts, "speakers") and tts.speakers:
            default_speaker = tts.speakers[0]  # assuming the first is the default
            CoquiTTSModel.log_warning("CoquiTTSModel", f"No speaker specified. Using default speaker: {default_speaker}")
            speaker = default_speaker

        return {
            "tts"               : tts,
            "speed"             : speed,
            "energy"            : energy,
            "speaker"           : speaker,
            "speaker_wav"       : speaker_wav,
            "language"          : language
        }

    # Generates speech based on provided parameters
    def text_to_speech(self, action):
        """Synthesize the speech from current text and other settings."""
        output_audio_path   = action.get("output-audio-path")
        
        tts_settings = self.resolve_model_settings(action)
        
        tts = tts_settings["tts"]
        from src.models.domain          import AudioModel
        text = TextModel.resolve_text_input(action, "text", "input-text-path", "input-text-reference")
        
        kwargs = {
            "text"              : text,
            "speed"             : tts_settings["speed"],
            "energy"            : tts_settings["energy"],
            "speaker"           : tts_settings["speaker"],
            "speaker_wav"       : tts_settings["speaker_wav"],
            "language"          : tts_settings["language"],
            "file_path"         : output_audio_path
        }

        Utils.ensure_dir(output_audio_path)
        
        tts.tts_to_file(**kwargs)
        from src.models.providers       import PyDubModel
        audio_data = PyDubModel.load_audio(output_audio_path)
        PyDubModel.resolve_audio_output(action, audio_data)