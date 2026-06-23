
from src.models.domain      import AudioModel
from src.helpers.core       import Utils
from pydub                  import AudioSegment

class PyDubModel(AudioModel):
    def __init__(self):
        super().__init__()

    # combines provided audios into one final audio
    def merge_audios(self, action):
        input_audio_paths           = action.get("input-audio-paths")
        input_audio_references      = action.get("input-audio-references")

        segments = []

        # Load audio from file paths
        if input_audio_paths:
            for file_path in input_audio_paths:
                segment = PyDubModel.load_audio(file_path)
                if segment:
                    segments.append(segment)

        # Load audio from cache
        if input_audio_references:
            for audio_reference in input_audio_references:
                segment = PyDubModel.load_from_cache("audio", audio_reference)
                if segment:
                    segments.append(segment)

        if segments:
            final_audio = sum(segments)
            PyDubModel.resolve_audio_output(action, final_audio)
        else:
            PyDubModel.log_error("PyDubModel", "No valid audio segments found to merge.")

    # creates an audio containing no sounds
    def create_silence(self, action):
        duration                    = action.get("duration", 1.00)

        audio_silence = AudioSegment.silent(duration=duration * 1000)
        PyDubModel.resolve_audio_output(action, audio_silence)

    # splits provided audio in more audios
    def split_audio(self, action):
        output_audio_path   = action.get("output-audio-path")
        split_times         = action.get("split-times", [])

        audio_data = PyDubModel.resolve_audio_input(action)
        audio_length_sec = len(audio_data) / 1000.0  # duration in seconds

        # Filter valid split times
        valid_split_times = []
        for t in sorted(split_times):
            if 0 < t < audio_length_sec:
                valid_split_times.append(t)
            else:
                PyDubModel.log_warning("PyDubModel", f"Ignoring out-of-range split time: {t}")

        valid_split_times.append(audio_length_sec)  # ensure final split

        # Split and save chunks
        PyDubModel.log_info("PyDubModel", f"Splitting audio at: {valid_split_times}")
        start_ms = 0

        for idx, split_time in enumerate(valid_split_times):
            end_ms = int(split_time * 1000)
            chunk = audio_data[start_ms:end_ms]

            part_path = f"{output_audio_path}_part{idx+1}.wav"
            PyDubModel.save_audio(chunk, part_path)

            start_ms = end_ms

