🏥 Confido Clinic Voice Assistant

A voice-enabled virtual receptionist built with FastAPI, Whisper (STT), ElevenLabs (TTS), and Llama3.1 (via Ollama).
It simulates a phone call experience: greeting the user, transcribing speech, generating natural responses with an LLM, and replying with synthesized voice.

🚀 Features

🎙️ Speech-to-Text: Converts your speech into text using Whisper (faster-whisper).

🧠 LLM-powered Responses: Uses Llama3.1 (Ollama) to generate natural, context-aware answers.

🔊 Text-to-Speech: Converts replies to voice with ElevenLabs API.

📅 Appointment Scheduling: Handles new or follow-up appointments with doctors.

🛡️ Insurance Queries: Answers whether specific insurance providers are accepted.

ℹ️ FAQs: Provides clinic hours, location, and contact details.

🌐 Web Frontend: A simple interface simulating a phone call.

🛠 Installation & Setup
1. Clone the Repository
git clone https://github.com/<your-username>/confido-clinic-assistant.git
cd confido-clinic-assistant

2. Create and Activate Virtual Environment

Windows (PowerShell):
```
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies
```
pip install -r requirements.txt
```

🔑 API Key Configuration

Create a file named .env in the project root.

Add your ElevenLabs API key inside:
```
ELEVENLABS_API_KEY=your_api_key_here
```

🦙 Setup Llama3.1 with Ollama
```
Install Ollama
 on your system.
Pull the Llama3.1 model:

ollama pull llama3.1
```

Test it:
```
ollama run llama3.1 "Hello, who are you?"
```
▶️ Running the Application

Start the backend:
```
uvicorn main1:app --reload
```

Backend runs at: http://127.0.0.1:8000

Open the frontend (index.html) in your browser:

Click Start Call → the AI assistant greets you.

Speak into your microphone → transcription + response + synthesized voice.

📂 Project Structure
confido-clinic-assistant/
│
├── main1.py                # FastAPI backend
├── backend/
│   ├── __init__.py
│   ├── stt_service.py      # Speech-to-text (Whisper)
│   ├── tts_service.py      # Text-to-speech (ElevenLabs)
│   ├── llm_service.py      # Llama3.1 integration (Ollama)
│
├── index.html              # Web frontend
├── requirements.txt
├── .env                    # Environment variables (ignored in Git)
└── .gitignore

📝 Example Conversation

Assistant: Hello! You’ve reached Confido Health Clinic. How may I help you today?
User: I want to book an appointment with Dr. Singh.
Assistant: Sure! Would this be a new appointment or a follow-up?
User: A new appointment.
Assistant: Great, when would you like to schedule it?

⚠️ Notes

STT: faster-whisper auto-detects language, CPU/GPU fallback.

TTS: requires an ElevenLabs API key.

LLM: powered by Llama3.1 (local inference via Ollama).

Frontend: plain HTML + JS, simulates a phone call flow.
