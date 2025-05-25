import os
import time
import shutil
import tempfile
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from faster_whisper import WhisperModel
from pydub.utils import mediainfo

logger = logging.getLogger("faster-whisper-api")

model = WhisperModel("small", device="auto", compute_type="int8")
executor = ThreadPoolExecutor(max_workers=4)

def _transcribe_sync(path: str, language: str):
    segments, _ = model.transcribe(
        path,
        language=language,
        beam_size=5,
        best_of=5,
        task="transcribe"
    )
    return "".join([seg.text for seg in segments])

def _get_audio_metadata(path: str):
    try:
        info = mediainfo(path)
        duration = float(info.get("duration", 0))
        return duration
    except Exception as e:
        logger.warning(f"Could not read audio metadata: {e}")
        return 0.0

def _human_readable_size(size_in_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"

async def transcribe_speech(speech_file, language: str = None) -> str:
    suffix = os.path.splitext(speech_file.filename)[-1] or ".mp3"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(speech_file.file, tmp)
        temp_path = tmp.name

    try:
        loop = asyncio.get_event_loop()

        # Metadata
        file_size_bytes = os.path.getsize(temp_path)
        file_size_hr = _human_readable_size(file_size_bytes)
        duration_sec = _get_audio_metadata(temp_path)

        inference_start = time.time()

        transcript = await loop.run_in_executor(
            executor,
            _transcribe_sync,
            temp_path,
            language
        )

        inference_time = (time.time() - inference_start) * 1000  # ms

        logger.info(
            f"Transcription done in {inference_time:.2f}ms | FILE_SIZE={file_size_hr} | AUDIO_DURATION={duration_sec:.2f}s"
        )

        return transcript.strip(), inference_time

    finally:
        os.remove(temp_path)
