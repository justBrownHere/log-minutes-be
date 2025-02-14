from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from utilize import trim_audio, format_diarization_result
from transcription import transcribe_audio
import os
from fastapi.responses import JSONResponse
import tempfile
from diarization import diarize_audio


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.post("/diarize")
async def diarize(audio_file: UploadFile = File(...))->list:
    try:
        results = []
        dia = diarize_audio(audio_file)
        diarization_result = format_diarization_result(dia)
        for dia in diarization_result:
            output_file_path = trim_audio(audio_file, dia['speaker'] ,dia["start_time"], dia["end_time"])
            audio_transcription = open(output_file_path, "rb")
            trancrible = transcribe_audio(audio_transcription)
            results.append({
                'speaker': dia['speaker'],
                'content': trancrible,
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diarization API Error: {str(e)}")
    return JSONResponse(
        content={
            "results": results
        }
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
        raise HTTPException(status_code=500, detail=f"Transcription API error: {str(e)}")
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
    