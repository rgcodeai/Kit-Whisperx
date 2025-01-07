import gradio as gr
import torch
from src.transcriber import transcribe_audio, LANGUAGE_OPTIONS
from src.model_manager import MODELS

def build_interface():
        
    def get_tab_label(fmt):
        return {"txt": "Plain Text", "vtt": "VTT", "srt": "SRT", "json": "JSON"}[fmt]

    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        # Header
        with gr.Row(equal_height=True):
            with gr.Column():
                gr.Markdown("# 🎙️ WhisperX Audio Transcription")
                gr.Markdown("❤️ Follow us on [YouTube](https://www.youtube.com/channel/UC_YzjCh-CSSCSGANvt5wBNQ?sub_confirmation=1), [GitHub](https://github.com/rgcodeai) 🌐 More on [Mister Contenidos](https://mistercontenidos.com)")
        
        # Main content
        with gr.Row():
            # Left column - Input and Configuration
            with gr.Column(variant="panel"):
                gr.Markdown("### 📁 Input File")
                gr.Markdown("Supported Formats: (mp3, mp4, wav, avi, mov, flv, mkv, webm)")
                with gr.Group():
                    file_input = gr.File(
                        label="Upload Audio/Video File",
                        file_types=["audio", "video"],
                        file_count="single",
                    )
                    
                    # Audio preview component
                    audio_player = gr.Audio(
                        label="Audio Preview",
                        type="filepath",
                        interactive=False,
                        visible=False
                    )
                gr.Markdown("### ⚙️ Configuration")
                with gr.Group():
                    language_dropdown = gr.Dropdown(
                        choices=list(LANGUAGE_OPTIONS.keys()),
                        label="Language",
                        value="Identify",
                    )
                    model_dropdown = gr.Dropdown(
                        choices=MODELS,
                        label="Model",
                        value="medium",
                    )
                    device_dropdown = gr.Dropdown(
                        choices=["cuda", "cpu"],
                        label="Device",
                        value="cuda" if torch.cuda.is_available() else "cpu",
                    )
                
                transcribe_button = gr.Button("▶️ Start Transcription", variant="primary")

            # Right column - Status and Output
            with gr.Column(variant="panel"):
                time_output = gr.Textbox(
                    label="Status",
                    placeholder="Ready to transcribe...",
                    interactive=False,
                )
                
                gr.Markdown("### 📝 Transcription Output")
                with gr.Tabs() as tabs:
                    output_components = {}
                    download_buttons = {}
                    file_components = {}
                    
                    for fmt in ["txt", "vtt", "srt", "json"]:
                        with gr.TabItem(get_tab_label(fmt)):
                            output_components[fmt] = gr.TextArea(
                                label=f"{fmt.upper()} Transcription",
                                interactive=False,
                                show_copy_button=True,
                            )
                            with gr.Row():
                                download_buttons[fmt] = gr.Button(f"⬇️ Download {fmt.upper()}")
                                file_components[fmt] = gr.File(
                                    label=f"{fmt.upper()} File",
                                    visible=False
                                )

        # Function to update audio player when file is uploaded
        def update_audio_preview(file):
            if file and file.name.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
                return gr.update(value=file.name, visible=True)
            return gr.update(visible=False)

        # Function to process transcription
        def start_process(file, language, model_name, device):
            if not file:
                return [gr.update(value="Please upload a file first.")] * 9
            
            try:
                results = transcribe_audio(file, language, model_name, device)
                return (
                    results[0],  # txt
                    results[4],  # txt_file
                    results[1],  # vtt
                    results[5],  # vtt_file
                    results[2],  # srt
                    results[6],  # srt_file
                    results[3],  # json
                    results[7],  # json_file
                    results[8],  # time
                )
            except Exception as e:
                error_msg = f"Error during transcription: {str(e)}"
                return [gr.update(value=error_msg)] * 9

        # Event handlers
        file_input.change(
            fn=update_audio_preview,
            inputs=[file_input],
            outputs=[audio_player]
        )

        transcribe_button.click(
            fn=start_process,
            inputs=[file_input, language_dropdown, model_dropdown, device_dropdown],
            outputs=[
                output_components["txt"], file_components["txt"],
                output_components["vtt"], file_components["vtt"],
                output_components["srt"], file_components["srt"],
                output_components["json"], file_components["json"],
                time_output
            ]
        )

        # Download button handlers
        for fmt in ["txt", "vtt", "srt", "json"]:
            download_buttons[fmt].click(
                fn=lambda x: gr.update(value=x, visible=True) if x else gr.update(visible=False),
                inputs=[file_components[fmt]],
                outputs=[file_components[fmt]]
            )

        return interface

if __name__ == "__main__":
    interface = build_interface()
    interface.launch()
