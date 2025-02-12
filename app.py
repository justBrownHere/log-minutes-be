from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from utilize import trim_audio
from transcription import transcribe_audio
import os
import datetime
from fastapi.responses import JSONResponse
import tempfile

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.post("/transcribe")
async def transcrible(audio_file: UploadFile = File(...))->str:
    try:
        suffix = os.path.splitext(audio_file.filename)[1] if audio_file.filename else ""
        with tempfile.NamedTemporaryFile(delete=False, suffix = suffix) as tmp_audio:
            content = await audio_file.read()
            tmp_audio.write(content)
            tmp_audio_path = tmp_audio.name
            transcribe_text = transcribe_audio(tmp_audio_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
    finally:
        if 'tmp_audio_path' in locals() or os.path.exists(tmp_audio_path):
            os.remove(tmp_audio)

    return JSONResponse(
        conntent={
            "transcription": transcribe_text
        })

@app.get("/")
async def root():
    return {"message": "Log Metting Transcription"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    