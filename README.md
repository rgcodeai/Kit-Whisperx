# **WhisperX Local Installation Kit**

## **Description**

This project enables the local installation and use of WhisperX, an advanced audio transcription system based on OpenAI's Whisper but optimized for running on local hardware with or without a GPU. This project is made possible thanks to [Whisperx](https://github.com/m-bain/whisperX) and [Faster Whisper](https://github.com/SYSTRAN/faster-whisper). This document provides a general overview of the installation and links to the website where the [complete installation and usage](https://mistercontenidos.com/en/how-to-install-whisperx-locally) procedure for this project can be found.

## **Requirements**

- Miniconda
- CUDA (only for NVIDIA GPU users)

## **File Description**

- **`environment-cuda.yml`**: Configuration file for automatic installation on systems with NVIDIA GPU.
- **`environment-cpu.yml`**: Configuration file for automatic installation on systems without NVIDIA GPU.
- **`app.py`**: Script to run the WhisperX user interface on Gradio.
- **`transcription_utils.py`**: Transcription logic.

## **Installation**

1. **Miniconda**: [Miniconda Installation](https://docs.anaconda.com/free/miniconda/)
2. **CUDA**: [CUDA Installation](https://developer.nvidia.com/cuda-toolkit-archive) (Only for NVIDIA GPU users)
3. **GitHub Repository**: Download and setup of the repository. See details on our website.

For a detailed step-by-step installation process, please visit our website: [View complete installation process](https://mistercontenidos.com/en/how-to-install-whisperx-locally)

## **Usage**

To use WhisperX after completing the installation:

1. Activate the corresponding Conda environment.
2. Run **`python app.py`** to start the Gradio user interface.

## **Authors**

- [MISTER CONTENTS](https://mistercontenidos.com/)
- [Ricardo Gonzalez](https://www.linkedin.com/in/pedrocuervomkt/)

## **Languages**

- [Spanish](docs/README_ES.md)
- [Portuguese](docs/README_PT.md)