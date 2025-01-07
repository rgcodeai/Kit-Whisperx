import os
import subprocess
import mimetypes
import json

# Constants
SUPPORTED_EXTENSIONS = ('.mp3', '.mp4', '.wav', '.avi', '.mov', '.flv', '.mkv', '.webm')
TEMP_DIR = os.path.join(os.getcwd(), 'Temp')
TEMP_AUDIO_FILE = os.path.join(TEMP_DIR, "temp_audio.wav")

def _create_temp_directory():
    """Creates the temporary directory if it doesn't exist."""
    os.makedirs(TEMP_DIR, exist_ok=True)

def is_valid_multimedia_file(file_path):
    """Checks if the file path corresponds to a valid multimedia file."""
    normalized_path = os.path.normpath(file_path)
    mime_type, _ = mimetypes.guess_type(normalized_path)
    is_supported_mime = mime_type and (mime_type.startswith('audio') or mime_type.startswith('video'))
    return is_supported_mime or normalized_path.lower().endswith(SUPPORTED_EXTENSIONS)

def validate_multimedia_file(file_path):
    """Validates if the file is a supported multimedia file."""
    if not is_valid_multimedia_file(file_path):
        raise ValueError("The uploaded file is not a valid multimedia file. Please upload a compatible audio or video file.")
    return file_path

def convert_to_wav(input_file):
    """Converts the input multimedia file to WAV format."""
    _create_temp_directory()
    command = [
        "ffmpeg", "-i", input_file, "-vn", "-ac", "1", "-ar", "16000", "-y", TEMP_AUDIO_FILE
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        error_message = f"Error during conversion: {e.stderr.decode()}"
        print(error_message)
        raise ValueError(f"Could not convert the file to WAV format. Ensure the file is valid and ffmpeg is installed. Details: {error_message}")
    return TEMP_AUDIO_FILE

def format_time(time_in_seconds, format_type="vtt"):
    """Formats time in seconds to a readable time format."""
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)

    if format_type == "srt":
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
    else:  # vtt
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def save_transcription(segments, file_format):
    """Saves the transcription in the specified format."""
    _create_temp_directory()
    file_path = os.path.join(TEMP_DIR, f'transcription_output.{file_format}')
    with open(file_path, 'w', encoding='utf-8') as file:
        if file_format == "txt":
            file.writelines(f"{segment['text'].strip()}\n" for segment in segments)
        elif file_format == "vtt":
            file.write("WEBVTT\n\n")
            file.writelines(f"{i+1}\n{format_time(segment['start'], 'vtt')} --> {format_time(segment['end'], 'vtt')}\n{segment['text'].strip()}\n\n" for i, segment in enumerate(segments))
        elif file_format == "srt":
            file.writelines(f"{i+1}\n{format_time(segment['start'], 'srt')} --> {format_time(segment['end'], 'srt')}\n{segment['text'].strip()}\n\n" for i, segment in enumerate(segments))
        elif file_format == "json":
            json.dump({"segments": segments}, file, ensure_ascii=False, indent=4)
    return file_path

def cleanup(device, input_file_path):
    """Performs cleanup of temporary files and cache."""
    if os.path.exists(TEMP_AUDIO_FILE) and input_file_path != TEMP_AUDIO_FILE:
        try:
            os.remove(TEMP_AUDIO_FILE)
        except OSError as e:
            print(f"Error deleting temporary file: {e}")

    if device == "cuda":
        import torch
        torch.cuda.empty_cache()
    import gc
    gc.collect()
