
from src.models.domain          import AudioModel
from src.helpers.core           import Utils
import whisper

class WhisperSTTModel(AudioModel):
    def __init__(self):
        super().__init__()

    # generates a transcript from provided audio
    def audio_to_text(self, action) -> str:
        whisper_model           = action.get("whisper-model")
        output_text_path        = action.get("output-text-path")
        
        temp_file = output_text_path + ".wav"
        from src.models.providers       import PyDubModel
        audio_data = PyDubModel.resolve_audio_input(action)
        PyDubModel.save_audio(audio_data, temp_file)
        
        model = whisper.load_model(whisper_model)
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
        
        Utils.delete_file(temp_file) # delete temporary file
        from src.models.domain          import TextModel
        TextModel.resolve_text_output(action, transcript_text)