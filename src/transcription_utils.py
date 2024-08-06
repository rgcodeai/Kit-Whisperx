import whisperx
import json
import os
import torch
import mimetypes
import shutil

# Define language options
language_options = {
    "Identify": None,
    "English": "en", "Spanish": "es", "Chinese": "zh", "Hindi": "hi", "Arabic": "ar",
    "Portuguese": "pt", "Bengali": "bn", "Russian": "ru", "Japanese": "ja", "Punjabi": "pa",
    "German": "de", "Javanese": "jv", "Wu Chinese": "zh", "Malay": "ms", "Telugu": "te",
    "Vietnamese": "vi", "Korean": "ko", "French": "fr", "Marathi": "mr", "Turkish": "tr"
}


# Available models for transcription
model_options = {
    "Large-v2": "large-v2",
    "Medium": "medium",
    "Small": "small",
    "Base": "base"
}

# Initializes the ModelManager by setting default values and loading a model based on system capabilities (CUDA availability).

class ModelManager:
    def __init__(self):
        self.current_model = None
        self.current_model_name = None
        self.current_device = None
        if torch.cuda.is_available():
            default_device = "cuda"
            default_model = "Medium"
        else:
            default_device = "cpu"
            default_model = "Medium"
        self.load_model(default_model, default_device)

    def load_model(self, model_choice, device):
        if self.current_model is None or model_choice != self.current_model_name or device != self.current_device:
            print(f"Attempting to load model: {model_choice} on device: {device}")
            
            # Determine compute type based on device
            if device == "cpu":
                compute_type = "int8"
            else:
                compute_type = "float16"
            
            self.current_model = whisperx.load_model(model_options[model_choice], device, compute_type=compute_type)
            self.current_model_name = model_choice
            self.current_device = device
        else:
            print(f"Using already loaded model: {self.current_model_name} on device: {self.current_device}")
        return self.current_model
    
# Validates if the given file path corresponds to a multimedia file (audio or video) by checking MIME types and specific file extensions.
def validate_multimedia_file(file_path):
    file_path = os.path.normpath(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and (mime_type.startswith('audio') or mime_type.startswith('video')):
        return file_path
    else:
        if file_path.lower().endswith(('.mp3', '.mp4', '.wav', '.avi', '.mov', '.flv')):
            return file_path
        else:
            raise ValueError("The uploaded file is not a multimedia file. Please upload an appropriate audio or video file.")

# Transcribes a multimedia file
def transcribe(file_obj, device, language, model_choice, model_manager):
    """
    Transcribes a multimedia file using a specified model, handling file operations, 
    language identification, and transcription alignment, and outputs transcription in multiple formats.
    """
    _, ext = os.path.splitext(file_obj.name)
    temp_dir = os.path.join(os.getcwd(), 'Temp')
    
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    new_file_path = os.path.join(temp_dir, f'resource{ext}')

    shutil.copy(file_obj.name, new_file_path)

    model = model_manager.load_model(model_choice, device)
    
    validated_file_path = validate_multimedia_file(new_file_path)
    audio = whisperx.load_audio(validated_file_path)

    if language == "Identify":
        result = model.transcribe(audio)
        language_code = result["language"]
    else:
        language_code = language_options[language]
        result = model.transcribe(audio, language=language_code)

    model_a, metadata = whisperx.load_align_model(language_code=language_code, device=device)
    try:
        aligned_segments = []
        for segment in result["segments"]:
            aligned_segment = whisperx.align([segment], model_a, metadata, audio, device, return_char_alignments=False)
            aligned_segments.extend(aligned_segment["segments"])
    except Exception as e:
        print(f"Error during alignment: {e}")
        return None

    segments_output = {"segments": aligned_segments}
    json_output = json.dumps(segments_output, ensure_ascii=False, indent=4)
    json_file_path = download_json_interface(json_output, temp_dir)
    txt_path = save_as_text(aligned_segments, temp_dir)
    vtt_path = save_as_vtt(aligned_segments, temp_dir)
    srt_path = save_as_srt(aligned_segments, temp_dir)
    return json_file_path, txt_path, vtt_path, srt_path  

# Saves the transcription text of audio segments to a file in the specified temporary directory and returns the file path.
def save_as_text(segments, temp_dir):
    txt_file_path = os.path.join(temp_dir, 'transcription_output.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        for segment in segments:
            txt_file.write(f"{segment['text'].strip()}\n")  
    return txt_file_path


def save_as_vtt(segments, temp_dir):
    """
    Saves the transcription text as a .vtt file (Web Video Text Tracks format), 
    which includes timestamps for each segment, in the specified temporary directory and returns the file path.
    """
    vtt_file_path = os.path.join(temp_dir, 'transcription_output.vtt')
    with open(vtt_file_path, 'w', encoding='utf-8') as vtt_file:
        vtt_file.write("WEBVTT\n\n")
        for i, segment in enumerate(segments):
            start = segment['start']
            end = segment['end']
            vtt_file.write(f"{i}\n")
            vtt_file.write(f"{format_time(start)} --> {format_time(end)}\n")
            vtt_file.write(f"{segment['text'].strip()}\n\n")  
    return vtt_file_path

def download_json_interface(json_data, temp_dir):
    """
    Reads JSON-formatted transcription data, modifies and re-saves it in a neatly 
    formatted JSON file in the specified temporary directory, and returns the file path.
    """
    json_file_path = os.path.join(temp_dir, 'transcription_output.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_data = json.loads(json_data)  
        for segment in json_data['segments']:
            segment['text'] = segment['text'].strip()
        json_data = json.dumps(json_data, ensure_ascii=False, indent=4)  
        json_file.write(json_data)
    return json_file_path


def save_as_srt(segments, temp_dir):
    """
    Saves the transcription text as an .srt file (SubRip Subtitle format), 
    which includes numbered entries with start and end times and corresponding text for each segment, 
    in the specified temporary directory and returns the file path.
    """
    srt_file_path = os.path.join(temp_dir, 'transcription_output.srt')
    with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
        for i, segment in enumerate(segments):
            start = segment['start']
            end = segment['end']
            srt_file.write(f"{i+1}\n")
            srt_file.write(f"{format_time_srt(start)} --> {format_time_srt(end)}\n")
            srt_file.write(f"{segment['text'].strip()}\n\n")  
    return srt_file_path

# Converts a time value in seconds to a formatted string in the "hours:minutes:seconds,milliseconds" format, used for timestamps in VTT files.
def format_time(time_in_seconds):
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = time_in_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:06.3f}"

# Converts a time value in seconds to a formatted string suitable for SRT files, specifically in the "hours:minutes:seconds,milliseconds" format.
def format_time_srt(time_in_seconds):
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
