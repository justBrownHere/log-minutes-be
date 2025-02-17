from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from utilize import trim_audio, format_diarization_result
from transcription import transcribe_audio
import os
from fastapi.responses import JSONResponse
import tempfile
from diarization import diarize_audio
from post_processing import post_process_transcript



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
        suffix = os.path.splitext(audio_file.filename)[1] if audio_file.filename else ""
        with tempfile.NamedTemporaryFile(delete=False, suffix = suffix) as tmp_audio:
            content = await audio_file.read()
            tmp_audio.write(content)
            tmp_audio_path = tmp_audio.name
        dia = diarize_audio(tmp_audio_path)
        diarization_result = format_diarization_result(dia)

        prompt_context = ""

        for dia in diarization_result:
            output_file_path = trim_audio(tmp_audio_path, dia["start_time"], dia["end_time"])
            trancrible = transcribe_audio(output_file_path)
            prompt_context += trancrible + "\n" 
            system_prompt = f"""
            Your task is to correct any spelling discrepancies in the transcribed text.
            Only add necessary punctuation such as periods, commas, and capitalization, and use only the context provided.
            """
            results.append({
                'speaker': dia['speaker'],
                'start_time': dia['start_time'],
                'end_time': dia['end_time'],
                'content': post_process_transcript(trancrible, system_prompt),
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diarization API Error: {str(e)}")
    finally:
        if 'tmp_audio_path' in locals() or os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)
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
            os.remove(tmp_audio_path)

    return JSONResponse(
        content={
            "transcription": transcribe_text
        })


@app.get("/")
async def root():
    return {"message": "Log Metting Transcription"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    