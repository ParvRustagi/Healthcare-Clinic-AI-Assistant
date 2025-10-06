from faster_whisper import WhisperModel
import tempfile
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
model = WhisperModel("small.en", device="cpu")

async def transcribe_audio(file) -> str:

    logger.info("entering the transcribing method")
    # Save uploaded audio to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        data = await file.read()
        logging.info({len(data)})
        logging.info("reading the conents now...")
        temp.write(data)
        logging.info("writing the contents into a temp file")
        temp.flush()
        logging.info("flush")

    segments, _ = model.transcribe(temp.name)
    logging.info("transcribing the model")
    transcript = " ".join([segment.text for segment in segments])
    logging.info("joining the text")
    return transcript.strip()
