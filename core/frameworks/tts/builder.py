
import whisper

from core.frameworks.base   import BaseBuilder
from core.utils             import Utils
from pydub                  import AudioSegment
from TTS.api                import TTS

class TTSBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.audio          = None
        self.tts_model      = None

    def load_audio(self, source_path):
        try:
            self.logger.info(f"[TTSBuilder] Loading audio from: {source_path}")
            
            return AudioSegment.from_file(source_path)
        except Exception as e:
            self.logger.error(f"[TTSBuilder] Error while loading audio: {e}")
            return None

    def save_audio(self, audio, destination_path):
        try:
            self.logger.info(f"[TTSBuilder] Saving audio to: {destination_path}")
            
            Utils.ensure_dir(destination_path)
            
            audio.export(destination_path, format="wav")
        except Exception as e:
            self.logger.error(f"[TTSBuilder] Error while saving audio: {e}")

    def load(self, action) -> 'TTSBuilder':
        """Load audio from a given file or from cache."""
        input_audio_path    = action.get("input-audio-path")
        audio_name          = action.get("audio-name")
        
        if input_audio_path:
            self.audio = self.load_audio(input_audio_path)
        elif audio_name:
            self.audio = self.load_from_cache("audio", audio_name)
        else:
            self.logger.error("[TTSBuilder] No load source specified (file or cache).")
            
        return self

    def save(self, action) -> 'TTSBuilder':
        """Save audio to cache or to a given file."""
        audio_name          = action.get("audio-name")
        output_audio_path   = action.get("output-audio-path")
        
        if not (output_audio_path or audio_name):
            self.logger.error("[TTSBuilder] No save target specified (file or cache).")
            
        if output_audio_path:
            self.save_audio(self.audio, output_audio_path)

        if audio_name:
            self.save_to_cache("audio", audio_name, self.audio)
        return self

    def set_tts(self, tts) -> 'TTSBuilder':
        """Set tts model to be used with this builder."""
        if tts:
            self.tts_model = tts
        else:
            self.logger.error("[TTSBuilder] No tts model provided.")
            
        return self

    def to_speech(self, action) -> 'TTSBuilder':
        """Synthetyze the speech from current text and other settings."""
        speech_speed        = action.get("speech-speed", 1.0)
        speech_energy       = action.get("speech-energy", 1.0)
        speech_speaker      = action.get("speech-speaker", None)
        output_audio_path   = action.get("output-audio-path")
        
        text = self.get_text(action)
        
        kwargs = {
            "text": text,
            "file_path": output_audio_path,
            "speed": speech_speed,
            "energy": speech_energy,
            "speaker": speech_speaker
        }

        Utils.ensure_dir(output_audio_path)
        
        self.tts_model.tts_to_file(**kwargs)

        # Load the result into memory for further operations
        self.audio = self.load_audio(output_audio_path)
            
        return self

    def to_transcript(self, action) -> 'TTSBuilder':
        """Use Whisper to transcribe curent audio with word timestamps."""
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

    def create_silence(self, action) -> 'TTSBuilder':
        """Create silent audio file."""
        duration            = action.get("duration", 1.00)

        self.audio = AudioSegment.silent(duration=duration * 1000)
            
        return self

    def combine_audios(self, action) -> 'TTSBuilder':
        """Combine audio segments from file paths or cache keys into one audio."""
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