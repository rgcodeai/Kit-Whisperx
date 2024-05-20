# **Kit de Instalação Local WhisperX**

## **Descrição**

Este projeto possibilita a instalação e uso local do WhisperX, um avançado sistema de transcrição de áudio baseado no OpenAI Whisper, mas otimizado para execução em hardware local com ou sem GPU. Este projeto é possível graças ao [Whisperx](https://github.com/m-bain/whisperX) e ao [Faster Whisper](https://github.com/SYSTRAN/faster-whisper). Este documento oferece uma visão geral da instalação e o link para o site onde está disponível o [procedimento completo de instalação e uso deste projeto.](https://mistercontenidos.com/pt/como-instalar-o-whisperx-localmente)

## **Requisitos**

- Miniconda
- CUDA (apenas para usuários com GPU NVIDIA)

## **Descrição dos Arquivos**

- **`environment-cuda.yml`**: Arquivo de configuração para instalação automática em sistemas com GPU NVIDIA.
- **`environment-cpu.yml`**: Arquivo de configuração para instalação automática em sistemas sem GPU NVIDIA.
- **`app.py`**: Script para executar a interface de usuário do WhisperX no Gradio.
- **`transcription_utils.py`**: Lógica de transcrição.

## **Instalação**

1. **Miniconda**: [Instalação do Miniconda](https://docs.anaconda.com/free/miniconda/)
2. **CUDA**: [Instalação do CUDA](https://developer.nvidia.com/cuda-toolkit-archive) (Apenas para usuários com GPU NVIDIA)
3. **Repositório do GitHub**: Download e configuração do repositório. Veja detalhes em nosso site.

Para um processo de instalação detalhado passo a passo, por favor visite nosso site: [Ver processo de instalação completo](https://mistercontenidos.com/pt/como-instalar-o-whisperx-localmente)

## **Uso**

Para usar o WhisperX após completar a instalação:

1. Ative o ambiente Conda correspondente.
2. Execute **`python app.py`** para iniciar a interface de usuário do Gradio.

## **Autores**

- [MISTER CONTEÚDOS](https://mistercontenidos.com/)
- [Ricardo Gonzalez](https://www.linkedin.com/in/pedrocuervomkt/)

## **Idiomas**

- [Inglês](README.md)
- [Português](docs/pt/README_PT.md)