import whisperx
import torch
import os
from src.model_manager import model_manager
from src.utils import validate_multimedia_file, convert_to_wav, save_transcription, cleanup

LANGUAGE_OPTIONS = {
    "Identify": None,
    "English": "en", "Spanish": "es", "Chinese": "zh", "Hindi": "hi", "Arabic": "ar",
    "Portuguese": "pt", "Bengali": "bn", "Russian": "ru", "Japanese": "ja", "Punjabi": "pa",
    "German": "de", "Javanese": "jv", "Wu Chinese": "zh", "Malay": "ms", "Telugu": "te",
    "Vietnamese": "vi", "Korean": "ko", "French": "fr", "Marathi": "mr", "Turkish": "tr"
}

def load_audio_and_transcribe(file, language, model_name, device):
    """Loads the audio and performs transcription with WhisperX."""
    model = model_manager.load_model(model_name, device)
    validated_file_path = validate_multimedia_file(file)
    if not validated_file_path.lower().endswith((".wav", ".mp3", ".flac", ".ogg", ".aac")):
        validated_file_path = convert_to_wav(validated_file_path)

    audio = whisperx.load_audio(validated_file_path)
    transcribe_options = {}
    if language != "Identify":
        transcribe_options['language'] = LANGUAGE_OPTIONS[language]
    result = model.transcribe(audio, **transcribe_options)
    return result, audio

def align_transcription(segments, audio, language_code, device):
    """Aligns the transcription segments with the audio."""
    alignment_model, metadata = whisperx.load_align_model(language_code=language_code, device=device)
    aligned_segments = whisperx.align(segments, alignment_model, metadata, audio, device)["segments"]
    return aligned_segments

# Main function to transcribe audio
def transcribe_audio(file_path, language, model_name, device):
    """Main function to transcribe the audio."""
    output_data = {fmt: None for fmt in ["txt", "vtt", "srt", "json"]}
    output_files = {f"{fmt}_file": None for fmt in ["txt", "vtt", "srt", "json"]}
    output_data.update(output_files)
    output_data["time"] = None

    try:
        import time
        start_time = time.time()
        result, audio = load_audio_and_transcribe(file_path, language, model_name, device)
        language_code = result.get("language") or LANGUAGE_OPTIONS[language]  # Determine language code

        aligned_segments = align_transcription(result["segments"], audio, language_code, device)

        file_paths = {fmt: save_transcription(aligned_segments, fmt) for fmt in ["txt", "vtt", "srt", "json"]}

        transcription_time = time.time() - start_time

        for fmt, path in file_paths.items():
            with open(path, 'r', encoding='utf-8') as f:
                output_data[fmt] = f.read()
            output_data[f"{fmt}_file"] = path

        output_data["time"] = f"Transcription completed in {transcription_time:.2f} seconds."

        return list(output_data.values())

    except Exception as e:
        import gradio as gr
        error_message = f"Error during transcription: {str(e)}"
        print(error_message)
        raise gr.Error(error_message)
    finally:
        cleanup(device, file_path)
