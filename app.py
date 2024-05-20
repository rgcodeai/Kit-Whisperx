import gradio as gr
import torch
import time
import os
from src.transcription_utils import transcribe, language_options, model_options, ModelManager

class TranscriptionApp:
    def __init__(self):
        """
        Initializes an instance with a ModelManager for managing AI models,
        sets default device and model based on CUDA availability, 
        and prepares a Gradio app and outputs dictionary for UI interactions and storing results.
        """
        self.model_manager = ModelManager()
        self.default_device = "cuda" if torch.cuda.is_available() else "cpu"
        self.default_model = "Large-v2" if torch.cuda.is_available() else "Medium"
        self.app = gr.Blocks()
        self.outputs = {}  
        self.last_transcription_time = 0  

        # Crear carpeta Temp si no existe
        if not os.path.exists('Temp'):
            os.makedirs('Temp')

    def start_transcription(self, file, device, language, model):
        """Start transcription process."""
        start_time = time.time()

        try:
            results = transcribe(file, device, language, model, self.model_manager)
        except ValueError as e:
            return str(e), 0  

        end_time = time.time()
        self.last_transcription_time = round(end_time - start_time, 1)  

        if results:
            json_output, txt_path, vtt_path, srt_path = results
            self.outputs = {
                'TXT': txt_path,
                'SRT': srt_path,
                'JSON': json_output,
                'VTT': vtt_path                
            }
            return self.update_output_text('TXT'), self.last_transcription_time
        return "No transcription available.", self.last_transcription_time


    def update_output_text(self, format_choice):
        """Update the text area based on the format choice."""
        if format_choice and self.outputs.get(format_choice):
            file_path = self.outputs[format_choice]
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except FileNotFoundError:
                return "File not found."
        return "No file available or format not selected."

    # User interface for the transcription kit using Gradio
    def setup_ui(self):
        with self.app:
            gr.Markdown("# Kit Transcriptor Whisperx")
            gr.Markdown("❤️ Follow us on [YouTube](https://www.youtube.com/channel/UC_YzjCh-CSSCSGANvt5wBNQ?sub_confirmation=1), [GitHub](https://github.com/rgcodeai) 🌐 More on [Mister Contenidos](https://mistercontenidos.com)")  
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Supported Formats: Audio (mp3, wav) and Video (mp4, avi, mov, flv)")
                    file_input = gr.File(label="Upload your multimedia file", type="filepath")
                    device_dropdown = gr.Dropdown(label="Select device", choices=["cuda", "cpu"], value=self.default_device)
                    model_dropdown = gr.Dropdown(label="Select model", choices=list(model_options.keys()), value=self.default_model)
                    language_dropdown = gr.Dropdown(label="Select language", choices=list(language_options.keys()), value="Identify")
                    transcribe_button = gr.Button("Start Transcription")
                    
                with gr.Column():
                    transcription_time_display = gr.Textbox(label="Last Transcription Time (seconds)", interactive=False, lines=1)
                    format_choice = gr.Radio(['TXT', 'SRT', 'VTT', 'JSON'], label="Select format to view:", value='TXT')
                    output_text = gr.Textbox(label="File Content", interactive=False, lines=10)
                    download_button = gr.Button("Download Transcription")
                    format_choice.change(fn=self.update_output_text, inputs=format_choice, outputs=output_text, queue=True)
                    download_button.click(fn=lambda x: self.outputs.get(x), inputs=format_choice, outputs=gr.File())

            transcribe_button.click(fn=self.start_transcription, inputs=[file_input, device_dropdown, language_dropdown, model_dropdown], outputs=[output_text, transcription_time_display])

    def launch(self):
        """Launch the transcription application."""
        self.setup_ui()
        self.app.launch()


if __name__ == '__main__':
    app = TranscriptionApp()
    app.launch()