import os
import torch
import ollama
import numpy as np
import sounddevice as sd
from TTS.api import TTS
import threading
import queue
import re
import speech_recognition as sr 
# System Setup
device = "cuda" if torch.cuda.is_available() else "cpu"
os.environ["COQUI_TOS_AGREED"] = "1"

print("Loading JARVIS core systems...")
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
xtts_model = tts.synthesizer.tts_model

gpt_cond_latent, speaker_embedding = xtts_model.get_conditioning_latents(audio_path=["Jarvis.wav"])

text_queue = queue.Queue()
recognizer = sr.Recognizer()

def voice_worker():
    with sd.OutputStream(samplerate=24000, channels=1, dtype='float32') as stream:
        while True:
            sentence = text_queue.get()
            if sentence is None: break 
            
            chunks = xtts_model.inference_stream(
                sentence, "en", gpt_cond_latent, speaker_embedding,
                stream_chunk_size=100, enable_text_splitting=False
            )
            for chunk in chunks:
                stream.write(chunk.cpu().numpy().squeeze())
            text_queue.task_done()

def listen_for_voice():
    """Captures audio from mic and returns text."""
    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("[Processing Speech...]")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def ask_jarvis():
    messages = [{'role': 'system', 'content': 'You are JARVIS. Concise, British, and call me Sir.'}]
    
    threading.Thread(target=voice_worker, daemon=True).start()

    print("JARVIS is online and listening, Sir.")
    while True:
        user_input = listen_for_voice()
        
        if not user_input:
            continue
            
        print(f"You said: {user_input}")
        
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            text_queue.put("Goodbye, Sir.")
            break

        messages.append({'role': 'user', 'content': user_input})
        
        full_reply = ""
        buffer = ""
        
        stream = ollama.chat(model='llama3.2:1b', messages=messages, stream=True)
        
        for chunk in stream:
            token = chunk['message']['content']
            full_reply += token
            buffer += token
            
            if any(p in token for p in [".", "!", "?", "\n"]):
                clean_text = buffer.strip()
                if clean_text:
                    text_queue.put(clean_text)
                buffer = ""

        messages.append({'role': 'assistant', 'content': full_reply})


ask_jarvis()