from faster_whisper import WhisperModel
import os
import shutil
import tempfile

model = WhisperModel("small", device="auto", compute_type="int8")


async def transcribe_speech(uploaded_file, language: str = None) -> str:
    suffix = os.path.splitext(uploaded_file.filename)[-1] or ".mp3"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(uploaded_file.file, tmp)
        temp_path = tmp.name

    try:
        segments, info = model.transcribe(
            temp_path,
            language=language,
            beam_size=5,
            best_of=5,
            task="transcribe"
        )
        text = "".join(segment.text for segment in segments)
        return text.strip()

    finally:
        os.remove(temp_path)

