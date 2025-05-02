import time
from faster_whisper import WhisperModel
import os
import shutil
import tempfile

model = WhisperModel("small", device="auto", compute_type="int8")


async def transcribe_speech(speech_file, language: str = None) -> str:
    suffix = os.path.splitext(speech_file.filename)[-1] or ".mp3"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(speech_file.file, tmp)
        temp_path = tmp.name

    try:
        inference_start = time.time()
        segments, info = model.transcribe(
            temp_path,
            language=language,
            beam_size=5,
            best_of=5,
            task="transcribe"
        )
        inference_time = (time.time() - inference_start) * 1000 # Convert to milliseconds

        text = "".join(segment.text for segment in segments)
        transcript = text.strip()

        return transcript, inference_time

    finally:
        os.remove(temp_path)

