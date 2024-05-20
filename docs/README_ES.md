# WhisperX Local Installation Kit

## Descripción
Este proyecto permite la instalación y uso local de WhisperX, un avanzado transcriptor de audio basado en OpenAI Whisper pero optimizado para ejecución en hardware local con o sin GPU. Este proyecyo es posible gracias a [Whisperx](https://github.com/m-bain/whisperX) y [Faster Whisper](https://github.com/SYSTRAN/faster-whisper). En este documento se ofrece una descripción general de la instalación y la referencia al sitio web donde se encuentra el [procedimiento completo de instalación y uso](https://mistercontenidos.com/como-instalar-whisperx-en-local) de este proyecto.
## Rrequisitos
- Miniconda
- CUDA (solo para usuarios con GPU NVIDIA)

## Descripción de los archivos
- `environment-cuda.yml`: Archivo de configuración para la instalación automática en sistemas con GPU NVIDIA.
- `environment-cpu.yml`: Archivo de configuración para la instalación automática en sistemas sin GPU NVIDIA.
- `app.py`: Script para ejecutar la interfaz de usuario de WhisperX en Gradio.
- `transcription_utils.py`: Logica de trascripción.

## Instalación

1. **Miniconda**: [Instalación de Miniconda](https://docs.anaconda.com/free/miniconda/)
2. **CUDA**: [Instalación de CUDA](https://developer.nvidia.com/cuda-toolkit-archive) (Solo para usuarios con GPU NVIDIA)
3. **Repositorio de GitHub**: Descarga y configuración del repositorio. Ver detalles en nuestro sitio web.

Para un proceso de instalación detallado paso a paso, por favor visita nuestra página web: [Ver proceso de instalación completo](https://mistercontenidos.com/como-instalar-whisperx-en-local)

## Uso
Para usar WhisperX después de completar la instalación:
1. Activar el entorno Conda correspondiente.
2. Ejecutar `python app.py` para iniciar la interfaz de usuario de Gradio.

## Autores
- [MISTER CONTENIDOS](https://mistercontenidos.com/)
- [Ricardo Gonzalez](https://www.linkedin.com/in/pedrocuervomkt/)

## Languages

- [Ingles](README.md)
- [Português](docs/README_PT.md)