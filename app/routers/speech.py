from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.services.speech_service import transcribe_speech

router = APIRouter()

@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    language: str = Form(None)):
    try:
        text = await transcribe_speech(file, language=language)

        return {"text": text}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
