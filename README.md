# Confido Clinic Assistant

A voice-based healthcare clinic assistant built with FastAPI, Whisper (STT), ElevenLabs (TTS), and Llama3.1 (LLM via Ollama).

## Features
- Speech-to-text with Whisper (faster-whisper)
- Natural language responses via Llama3.1 (Ollama)
- Text-to-speech with ElevenLabs
- Appointment booking, insurance checks, FAQs
- Web interface simulating a phone call

## Setup
```bash
git clone https://github.com/ParvRustagi/Healthcare-Clinic-AI-Assistant.git
cd heathcare-clinic-assistant
python -m venv venv
venv\Scripts\activate   # on Windows
pip install -r requirements.txt
```

## RUN
uvicorn main1:app --reload

