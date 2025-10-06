import base64
import uuid
import logging
from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.stt_service import transcribe_audio
from backend.tts_service import synthesize_speech

app = FastAPI(title="Confido Health Voice Assistant")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}
appointments = {
    "Dr. Singh": ["2025-10-05 15:00"],
    "Dr. Patel": [],
}
insurance_db = {
    "BlueCross": {
        "covered_services": ["general checkup", "cleaning", "x-ray"],
        "in_network_doctors": ["Dr. Singh"]
    },
    "Aetna": {
        "covered_services": ["cleaning", "dental exam", "follow-up"],
        "in_network_doctors": ["Dr. Patel", "Dr. Singh"]
    }
}
clinic_info = {
    "name": "Confido Health Clinic",
    "hours": "Mon–Sat 9 AM–6 PM, closed Sundays",
    "address": "1245 West Green Street, Springfield, IL",
    "contact": "(217) 555-0138"
}

# ---------------------------
# Intent detection
# ---------------------------
def detect_intent(user_text: str):
    text = user_text.lower()
    if any(w in text for w in ["insurance", "covered", "aetna", "bluecross", "blue cross"]):
        return "insurance"
    if any(w in text for w in ["where", "location", "address", "hours", "open", "close", "contact", "phone"]):
        return "faq"
    if any(w in text for w in ["book", "schedule", "appointment", "follow", "new", "doctor"]):
        return "appointment"
    return "chitchat"

# ---------------------------
# Slot filling
# ---------------------------
def handle_appointment(session_id: str, user_text: str) -> str:
    s = sessions[session_id]
    slots = s["slots"]
    text = user_text.lower().strip()

    if s.get("last_user_text") == text:
        return "I noted that already. Could you add more details, like day and time?"
    s["last_user_text"] = text

    if "follow" in text or "check-up" in text:
        slots["appointment_type"] = slots["appointment_type"] or "follow-up"
    elif any(w in text for w in ["book", "schedule", "appointment", "new", "video"]):
        slots["appointment_type"] = slots["appointment_type"] or "new"

    for doc in appointments.keys():
        if doc.lower() in text:
            slots["doctor"] = slots["doctor"] or doc

    if any(tok in text for tok in ["am", "pm", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]):
        slots["datetime"] = slots["datetime"] or user_text

    if not slots["doctor"] and not slots["appointment_type"]:
        return "Sure, is this a new appointment or a follow-up, and which doctor would you like to see?"
    if slots["doctor"] and not slots["appointment_type"]:
        return f"Great — {slots['doctor']}. Is this a new appointment or a follow-up?"
    if slots["appointment_type"] and not slots["doctor"]:
        return "Got it. Which doctor would you like to see?"
    if slots["doctor"] and slots["appointment_type"] and not slots["datetime"]:
        return f"Got it — a {slots['appointment_type']} appointment with {slots['doctor']}. What day and time works for you?"
    if slots["doctor"] and slots["appointment_type"] and slots["datetime"]:
        return (f"Perfect — I'll tentatively place a {slots['appointment_type']} appointment with "
                f"{slots['doctor']} at '{slots['datetime']}'. Shall I confirm that?")
    return "Can you clarify if it’s new or follow-up and with which doctor?"

# ---------------------------
# Insurance Q&A
# ---------------------------
def handle_insurance(user_text: str) -> str:
    text = user_text.lower()
    for provider, data in insurance_db.items():
        if provider.lower() in text:
            covered = ", ".join(data["covered_services"])
            doctors = ", ".join(data["in_network_doctors"])
            return (f"Yes, we accept {provider}. It covers {covered}. "
                    f"In-network doctors are {doctors}.")
    return "We accept major insurances like Aetna and BlueCross. Which one do you have?"

# ---------------------------
# FAQ Q&A
# ---------------------------
def handle_faq(user_text: str) -> str:
    text = user_text.lower()
    if "where" in text or "address" in text or "location" in text:
        return f"Our clinic is located at {clinic_info['address']}."
    if "hours" in text or "open" in text or "close" in text:
        return f"We are open {clinic_info['hours']}."
    if "contact" in text or "phone" in text or "number" in text:
        return f"You can reach us at {clinic_info['contact']}."
    return "We are Confido Health Clinic, happy to help! You can ask about our hours, location, or contact."

# ---------------------------
# Routes
# ---------------------------
@app.get("/start")
async def start_conversation(session_id: str = Query(default=None)):
    session_id = session_id or str(uuid.uuid4())
    sessions[session_id] = {
        "history": [],
        "slots": {"appointment_type": None, "doctor": None, "datetime": None},
        "last_user_text": ""
    }
    greeting = "Hello! You’ve reached Confido Health Clinic. I’m your virtual assistant. How may I help you today?"
    audio_path = await synthesize_speech(greeting)
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    return JSONResponse({"reply": greeting, "audio": base64.b64encode(audio_bytes).decode("utf-8"), "session_id": session_id})

@app.post("/voice-assistant")
async def voice_assistant(file: UploadFile = File(...), session_id: str = Form("default")):
    logger.info("📥 Voice request received")
    user_text = await transcribe_audio(file)
    user_text_clean = (user_text or "").strip()

    if not user_text_clean:
        reply = "Sorry, I didn’t catch that. Could you say it again?"
    else:
        intent = detect_intent(user_text_clean)
        if intent == "appointment":
            reply = handle_appointment(session_id, user_text_clean)
        elif intent == "insurance":
            reply = handle_insurance(user_text_clean)
        elif intent == "faq":
            reply = handle_faq(user_text_clean)
        else:
            reply = "I’m here to help with appointments, insurance, or clinic info. What would you like to do?"

    sessions[session_id]["history"].append((user_text_clean, reply))
    audio_path = await synthesize_speech(reply)
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    return JSONResponse({"user_text": user_text_clean, "reply": reply, "audio": base64.b64encode(audio_bytes).decode("utf-8"), "session_id": session_id})