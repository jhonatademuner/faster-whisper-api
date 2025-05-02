from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.services.speech_service import transcribe_speech

router = APIRouter()

@router.post("/transcribe")
async def transcribe(
    speech_file: UploadFile = File(...),
    language: str = Form(None)):
    try:
        transcript, inference_time = await transcribe_speech(speech_file=speech_file, language=language)

        return {"transcript": transcript, "inference_time_ms": inference_time}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
