# English and Meitei Voice Translator

This project supports voice translation in both directions. It can record spoken English, translate it into Meitei, generate Meitei speech, and it can also translate Meitei speech into English Speech.

## Features

- Microphone recording in English
- Speech-to-text using Google Speech Recognition
- English to Meitei translation via an ONNX translation model
- Meitei to English translation via an ONNX translation model
- Meitei text-to-speech generation using Parler TTS
- Automatic playback of the generated WAV file

## Project Files

- `voice_translator.py` — interactive launcher for both translation directions
- `english_voice_to_meitei_voice.py` — main end-to-end pipeline
- `meitei_to_english_voice.py` — Meitei voice-to-English translation pipeline
- `meitei_to_english.py` — Meitei-to-English translation logic
- `translate_once.py` — wrapper script for translation execution
- `translator1.py` — English-to-Meitei translation model loader and logic
- `meitei_tts_generate.py` — Meitei TTS model loader and voice synthesis
- `requirements.txt` — Python package list

## Requirements

- Python 3.10 or newer
- A working microphone
- Internet access for speech recognition and Hugging Face model downloads
- NVIDIA GPU is optional, but the project supports CUDA if available

## Setup

Create and activate a virtual environment if desired, then install dependencies:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install fastapi uvicorn python-multipart SpeechRecognition sounddevice soundfile numpy scipy transformers parler-tts huggingface-hub sentencepiece onnxruntime tokenizers
```

If you are using CPU only, you can install the standard PyTorch package instead of the CUDA build.

## Run the Application

From the project folder, start the interactive translator:

```bash
python voice_translator.py
```

Choose an option from the menu:

1. `English -> Meitei` — records English speech, translates it into Meitei, generates Meitei speech, and plays the WAV output
2. `Meitei -> English` — records Meitei speech, translates it into English, generates English speech, and plays the WAV output
3. `Exit` — closes the launcher

You can also run either pipeline directly if needed:

```bash
python english_voice_to_meitei_voice.py
python meitei_to_english_voice.py
```

The English-to-Meitei pipeline will:

1. Record English speech for a few seconds
2. Convert it to English text
3. Translate the text into Meitei
4. Generate Meitei speech as a WAV file
5. Open the generated audio file for playback

## Output Files

- `english_input.wav` — recorded English voice
- `translated_meitei.wav` — final Meitei audio output

## Notes

- The microphone device index may need to be changed in `english_voice_to_meitei_voice.py` if your system has a different audio input.
- The first run may take longer because the translation and TTS models are downloaded from Hugging Face.
- If recognition fails, try speaking more clearly or check your microphone input.

## Example Workflow

```text
English spoken voice
    -> Speech recognition
    -> English text
    -> English to Meitei translation
    -> Meitei text
    -> Meitei speech generation
    -> WAV output playback
```

The launcher also supports the reverse workflow:

```text
Meitei spoken voice
    -> Speech recognition
    -> Meitei text
    -> Meitei to English translation
    -> English text
    -> English speech generation
    -> WAV output playback
```

## License

This project is provided as-is for educational and experimental use.
