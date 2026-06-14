
import numpy as np
import whisper

from core.frameworks.base   import BaseBuilder
from core.utils             import Utils
from pydub                  import AudioSegment
from TTS.api                import TTS
from TTS.utils.manage       import ModelManager

class TTSBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.audio          = None

    # load defaults for TTSBuilder class:
    # - reads default model-path
    # - initializes and stores a default TTS model at the class level
    @staticmethod
    def load_defaults(defaults):
        model_path          = defaults.get("model-path", "tts_models/multilingual/multi-dataset/your_tts")

        TTSBuilder.tts      = TTS(model_path)

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
            self.logger.debug(f"[TTSHandler] Initialized object's TTS model: {model_path}")
            tts = TTS(model_path)
        else:
            tts = TTSBuilder.tts

        # If no speaker specified but model has speakers, use default and warn
        if speaker is None and hasattr(tts, "speakers") and tts.speakers:
            default_speaker = tts.speakers[0]  # assuming the first is the default
            self.logger.warning(f"[TTSBuilder] No speaker specified. Using default speaker: {default_speaker}")
            speaker = default_speaker

        return {
            "tts"               : tts,
            "speed"             : speed,
            "energy"            : energy,
            "speaker"           : speaker,
            "speaker_wav"       : speaker_wav,
            "language"          : language
        }

    # Load audio:
    # - loads an audio file from specified source
    # - otherwise return None
    def load_audio(self, source_path):
        try:
            self.logger.info(f"[TTSBuilder] Loading audio from: {source_path}")
            
            return AudioSegment.from_file(source_path)
        except Exception as e:
            self.logger.error(f"[TTSBuilder] Error while loading audio: {e}")
            return None

    # Save audio:
    # - Saves provided audio file to specified destination
    def save_audio(self, audio, destination_path):
        try:
            self.logger.info(f"[TTSBuilder] Saving audio to: {destination_path}")
            
            Utils.ensure_dir(destination_path)
            
            audio.export(destination_path, format="wav")
        except Exception as e:
            self.logger.error(f"[TTSBuilder] Error while saving audio: {e}")

    # Default load function adapted to audio:
    # - loads an audio file from specified source
    # - loads an audio file from specified cache location
    def load(self, action, path_key="input-audio-path", cache_key="audio-name") -> 'TTSBuilder':
        input_audio_path    = action.get(path_key)
        audio_name          = action.get(cache_key)
        
        if input_audio_path:
            self.audio = self.load_audio(input_audio_path)
        elif audio_name:
            self.audio = self.load_from_cache("audio", audio_name)
        else:
            self.logger.error("[TTSBuilder] No load source specified (file or cache).")
            
        return self

    # Default save function adapted to audio:
    # - saves an audio file to specified destination
    # - saves an audio file to specified cache location
    def save(self, action, path_key="output-audio-path", cache_key="audio-name") -> 'TTSBuilder':
        audio_name          = action.get(cache_key)
        output_audio_path   = action.get(path_key)
        
        if not (output_audio_path or audio_name):
            self.logger.error("[TTSBuilder] No save target specified (file or cache).")
            
        if output_audio_path:
            self.save_audio(self.audio, output_audio_path)

        if audio_name:
            self.save_to_cache("audio", audio_name, self.audio)
        return self

    # Generate trasncript function:
    # - uses whisper to generate a word by word transcript
    def generate_transcript(self, action) -> 'TTSBuilder':
        output_text_path        = action.get("output-text-path")
        
        temp_file = output_text_path + ".wav"
        self.save_audio(self.audio, temp_file)
        
        model = whisper.load_model("base")
        result = model.transcribe(temp_file, word_timestamps=True)

        words_info = []
        for segment in result['segments']:
            for word_info in segment['words']:
                words_info.append({
                    'word': word_info['word'],
                    'start_time': word_info['start'],
                    'end_time': word_info['end']
                })

        # Format each word as a separate subtitle line
        transcript_text = ""
        for i, word_info in enumerate(words_info, 1):
            start_time  = Utils.format_time(word_info['start_time'])
            end_time    = Utils.format_time(word_info['end_time'])
            word = word_info['word'].strip()
            transcript_text += f"{i}\n{start_time} --> {end_time}\n{word}\n\n"
        
        #Delete temporary file
        Utils.delete_file(temp_file)
        #Now save the transcript
        self.save_text(transcript_text, output_text_path)
            
        return self

    # Generate transcript function:
    # - reads audios from disk and adds them to combine list
    # - reads audios from cache and adds them to combine list
    # - takes all audios from combine list and combines them in one final audio file
    def combine_audios(self, action) -> 'TTSBuilder':
        input_audio_paths   = action.get("input-audio-paths")
        audio_names         = action.get("audio-names")

        segments = []

        # Load audio from file paths
        if input_audio_paths:
            for file_path in input_audio_paths:
                segment = self.load_audio(file_path)
                if segment:
                    segments.append(segment)

        # Load audio from cache
        if audio_names:
            for audio_name in audio_names:
                segment = self.load_from_cache("audio", audio_name)
                if segment:
                    segments.append(segment)

        if not segments:
            self.logger.error("[TTSBuilder] No valid audio segments found to merge.")
            return self

        self.audio = sum(segments)
        return self

    # Create silence function:
    # - creates a silenced audio of specified duration
    def create_silence(self, action) -> 'TTSBuilder':
        duration            = action.get("duration", 1.00)

        self.audio = AudioSegment.silent(duration=duration * 1000)
            
        return self

    # show-models command:
    # - shows available TTS models
    def show_models(self, action) -> 'TTSBuilder':
        ModelManager().list_models()

        return self

    # show-speakers command:
    # - shows speakers for specific TTS model
    def show_speakers(self, action) -> 'TTSBuilder':
        settings = self.resolve_model_settings(action)
        tts = settings["tts"]

        if hasattr(tts, "speakers") and tts.speakers:
            for speaker in tts.speakers:
                self.logger.info(f" - {speaker}")
        else:
            self.logger.info("[TTSBuilder] This model does not provide speaker IDs.")

        return self

    # split-audio command:
    # - loads the target audio
    # - splits it in more audios
    def split_audio(self, action) -> 'TTSBuilder':
        output_audio_path   = action.get("output-audio-path")
        split_times         = action.get("split-times", [])

        if not output_audio_path:
            self.logger.error("[TTSBuilder] No output audio path provided.")
            return self

        audio = self.audio
        audio_length_sec = len(audio) / 1000.0  # duration in seconds

        # Filter valid split times
        valid_split_times = []
        for t in sorted(split_times):
            if 0 < t < audio_length_sec:
                valid_split_times.append(t)
            else:
                self.logger.warning(f"[TTSBuilder] Ignoring out-of-range split time: {t}")

        valid_split_times.append(audio_length_sec)  # ensure final split

        # Split and save chunks
        self.logger.info(f"[TTSBuilder] Splitting audio at: {valid_split_times}")
        start_ms = 0

        for idx, split_time in enumerate(valid_split_times):
            end_ms = int(split_time * 1000)
            chunk = audio[start_ms:end_ms]

            part_path = f"{output_audio_path}_part{idx+1}.wav"
            self.save_audio(chunk, part_path)

            start_ms = end_ms

        return self

    # Generates speech based on provided parameters
    def text_to_speech(self, action) -> 'TTSBuilder':
        """Synthesize the speech from current text and other settings."""
        output_audio_path   = action.get("output-audio-path")
        
        tts_settings = self.resolve_model_settings(action)
        
        tts = tts_settings["tts"]
        
        text = self.get_text(action)
        
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

        # Load the result into memory for further operations
        self.audio = self.load_audio(output_audio_path)
            
        return self

