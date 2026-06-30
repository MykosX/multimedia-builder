
# src/models/providers/audio.py

from pydub                      import AudioSegment

from src.models.core            import BaseHelper
from src.utils                  import Logger, Utils

from TTS.api                    import TTS

class AudioHelper(BaseHelper):
    def __init__(self, audio_segment=None):
        self.audio_segment = audio_segment or AudioSegment.silent(0)

    def get_audio(self) -> AudioSegment:
        return self.audio_segment

    # loads an audio file from specified source
    def load(self, source_path) -> AudioHelper:
        try:
            Logger.log_info("AudioHelper", f"Loading audio from: {source_path}")

            self.audio_segment = AudioSegment.from_file(source_path)

        except Exception as e:
            Logger.log_error("AudioHelper", f"Error while loading audio: {e}")
            self.audio_segment = AudioSegment.silent(0)

        return self

    # saves provided audio file to specified destination
    def save(self, destination_path, format="wav") -> AudioHelper:
        try:
            Logger.log_info("AudioHelper", f"Saving audio to: {destination_path}")

            Utils.ensure_dir(destination_path)

            self.audio_segment.export(destination_path, format=format)

        except Exception as e:
            Logger.log_error("AudioHelper", f"Error while saving audio: {e}")

        return self

    # resolves the input as audio: a) read from a file or c) read from cache
    def resolve_input(self, input_audio_path, input_audio_reference) -> AudioHelper:
        if input_audio_path:
            audio_helper = AudioHelper().load(input_audio_path)
        elif input_audio_reference:
            audio_helper = AudioHelper.load_from_cache("audio", input_audio_reference)
        else:
            Logger.log_error("AudioHelper", f"No load source specified (file:'{input_audio_path}' or reference:'{input_audio_reference}').")
            audio_helper = AudioHelper()

        return audio_helper

    # resolves the output as audio: a) writes to a file or b) saves to cache
    def resolve_output(self, output_audio_path, output_audio_reference) -> AudioHelper:
        if not (output_audio_path or output_audio_reference):
            Logger.log_error("AudioHelper", f"No save target specified (file:'{output_audio_path}' or reference:'{output_audio_reference}').")
            return

        if output_audio_path:
            self.save(output_audio_path)

        if output_audio_reference:
            AudioHelper.save_to_cache("audio", output_audio_reference, self)
        
        return self

    def merge(self, audios: list["AudioHelper"]) -> AudioHelper:
        merged = AudioSegment.silent(0)

        for audio in audios:
            merged += audio.audio_segment

        return AudioHelper(merged)

    def with_silence(self, duration: float) -> AudioHelper:
        self.audio_segment += AudioSegment.silent(duration=duration * 1000)
        
        return self

    def split(self, split_times) -> list[AudioHelper]:
        audio_length_sec = len(self.audio_segment) / 1000.0

        # Filter valid split times
        valid_split_times = []
        for split_time in sorted(split_times):
            if 0 < split_time < audio_length_sec:
                valid_split_times.append(split_time)
            else:
                Logger.log_warning("AudioHelper", f"Ignoring out-of-range split time: {split_time}")

        # Always include the end of the audio.
        valid_split_times.append(audio_length_sec)

        Logger.log_info("AudioHelper", f"Splitting audio at: {valid_split_times}")

        chunks: list[AudioHelper] = []
        start_ms = 0
        
        for split_time in valid_split_times:
            end_ms = int(split_time * 1000)
            chunks.append(AudioHelper(self.audio_segment[start_ms:end_ms]))
            start_ms = end_ms
        
        return chunks

    def text_to_speech(self, text, tts_settings, output_audio_path) -> AudioHelper:
        model_path = tts_settings["model_path"] or "tts_models/en/ljspeech/vits"
        
        Logger.log_info("AudioHelper", f"Initialized Coqui TTS model: {model_path}")
        coqui_tts = TTS(model_path)
        
        speaker = tts_settings["speaker"]
        # If no speaker specified but model has speakers, use default and warn
        if speaker is None and hasattr(coqui_tts, "speakers") and coqui_tts.speakers:
            default_speaker = coqui_tts.speakers[0]  # assuming the first is the default
            Logger.log_warning("AudioHelper", f"No speaker specified. Using default speaker: {default_speaker}")
            speaker = default_speaker
        
        kwargs = {
            "text"              : text,
            "speed"             : tts_settings["speed"],
            "energy"            : tts_settings["energy"],
            "speaker"           : speaker,
            "speaker_wav"       : tts_settings["speaker_wav"],
            "language"          : tts_settings["language"],
            "file_path"         : output_audio_path
        }
        
        Utils.ensure_dir(output_audio_path)
        
        coqui_tts.tts_to_file(**kwargs)
        
        return AudioHelper().load(output_audio_path)
    