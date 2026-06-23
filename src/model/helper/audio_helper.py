
# -----------------------------------------------------------------------------
# src/model/helper/audio_helper.py
# -----------------------------------------------------------------------------

from collections.abc        import Iterable

from src.core               import Console

from pydub                  import AudioSegment

# -----------------------------------------------------------------------------
# AudioHelper
#
# * Gives access to specific audio IO functions
# * Provides access to audio transformations
# -----------------------------------------------------------------------------


class AudioHelper:
    # -------------------------------------------------------------------------
    # Audio IO
    # -------------------------------------------------------------------------

    @staticmethod
    def import_as() -> AudioSegment:
        pass

    @staticmethod
    def export_as() -> None:
        pass

    # -------------------------------------------------------------------------
    # General audio transformations
    # -------------------------------------------------------------------------

    @staticmethod
    def merge(audios: list[AudioSegment]) -> AudioSegment:
        merged = cls().audio

        for audio in audios:
            merged += audio.audio

        return merged

    @staticmethod
    def with_silence(audio: AudioSegment, duration: float = 1.0) -> AudioSegment:
        silence = AudioSegment.silent(duration=duration * 1000)

        if audio:
            return audio + silence
        else:
            return silence

    @staticmethod
    def split(audio: AudioSegment, split_times: Iterable[float] = [1.0, 2.0]) -> list[AudioSegment]:
        audio_length_sec = len(audio) / 1000.0

        # Filter valid split times
        valid_split_times = []
        for split_time in sorted(split_times):
            if 0 < split_time < audio_length_sec:
                valid_split_times.append(split_time)
            else:
                Console.warning(f"Ignoring out-of-range split time: {split_time}")

        # Always include the end of the audio.
        valid_split_times.append(audio_length_sec)

        Console.info(f"Splitting audio at: {valid_split_times}")

        chunks: list[AudioSegment] = []
        start_ms = 0
        
        for split_time in valid_split_times:
            end_ms = int(split_time * 1000)
            chunks.append(audio[start_ms:end_ms])
            start_ms = end_ms
        
        return chunks

# -----------------------------------------------------------------------------
