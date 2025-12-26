# JARVIS - AI Voice Assistant

A sophisticated voice-enabled AI assistant powered by Llama 3.2, featuring real-time text-to-speech with custom voice cloning. Chat with JARVIS as your personal British AI butler.

## Features

- **Real-time Voice Synthesis**: Stream audio while processing responses using XTTS-v2
- **Custom Voice Cloning**: Clone any voice from a reference audio file
- **Local LLM Integration**: Powered by Llama 3.2 (1B) for fast, privacy-focused responses
- **Streaming Chat**: Get responses streamed sentence-by-sentence for immediate feedback
- **Sentence-level Audio**: Automatic sentence segmentation ensures natural speech patterns

## Requirements

- Python 3.8+
- CUDA-capable GPU (recommended) or CPU fallback
- 8GB+ RAM (8GB works but barely)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Amaanish/jarvis.git
cd jarvis
```

2. Install dependencies:
```bash
pip install torch torchvision torchaudio
pip install ollama
pip install TTS
pip install sounddevice numpy
pip install SpeechRecognition
```

3. Pull the Llama 3.2 model:
```bash
ollama pull llama3.2:1b
```

4. Prepare your voice sample:
- Place a reference audio file named `Jarvis.wav` in the project directory (I have uploaded this file in the directory)
- The audio should be 30-60 seconds of clear speech for best results

## Usage

Run the assistant:
```bash
python jarvis.py
```

JARVIS will initialize and begin listening. Simply speak your commands or questions naturally. JARVIS will recognize your speech, process it, and respond with synthesized audio.

```
JARVIS is online and listening, Sir.
[Listening...]
[Processing Speech...]
You said: Hello JARVIS
JARVIS: Good morning, Sir. How may I be of assistance?
```

To exit, say any of: `exit`, `quit`, or `goodbye`.

## How It Works

**Voice Processing Pipeline:**
1. Microphone captures user speech
2. Google Speech-to-Text converts audio to text
3. User text is sent to Llama 3.2 for processing
4. Response is streamed token-by-token
5. Sentences are detected and queued for speech synthesis
6. XTTS-v2 converts text to speech using your custom voice
7. Audio is played in real-time while new text is being generated

**Architecture:**
- **STT**: Google Speech-to-Text API via SpeechRecognition library
- **LLM**: Llama 3.2 (1B) via Ollama for fast inference
- **TTS Engine**: XTTS-v2 (Coqui) for multilingual, high-quality speech synthesis
- **Voice Cloning**: Uses speaker embeddings extracted from reference audio
- **Threading**: Separate worker thread handles audio playback without blocking speech recognition

## Configuration

Edit the system prompt in `ask_jarvis()` to customize JARVIS's personality:
```python
'You are JARVIS. Concise, British, and call me Sir.'
```

Change the Ollama model by modifying:
```python
stream = ollama.chat(model='llama3.2:1b', messages=messages, stream=True)
```

## Performance Tips

- Use a GPU for faster TTS synthesis (`device` is auto-detected)
- Shorter audio samples (30-60 seconds) often work better for voice cloning
- Keep system prompt concise for faster responses
- Reduce stream chunk size if experiencing latency

## Troubleshooting

**No audio output:**
- Check that `sounddevice` can access your audio device
- Verify `Jarvis.wav` exists in the project directory

**Microphone not working:**
- Ensure your microphone is connected and recognized by your system
- Check microphone permissions for Python
- Test with: `python -m speech_recognition`

**Speech recognition issues:**
- Make sure you have a stable internet connection (Google Speech-to-Text requires it)
- Speak clearly and avoid background noise
- Adjust the `phrase_time_limit` and timeout values in `listen_for_voice()` if needed

**Slow responses:**
- Run with CUDA-capable GPU for better performance
- Consider using a faster quantized model

**Voice quality issues:**
- Ensure your reference audio is clear and noise-free
- Try different voice samples for better results


## Credits

- [Coqui TTS](https://github.com/coqui-ai/TTS) - XTTS-v2 synthesis
- [Ollama](https://ollama.ai/) - Local LLM inference
- [Meta](https://www.meta.com/) - Llama 3.2 model

---

*"At your service, Sir."*
