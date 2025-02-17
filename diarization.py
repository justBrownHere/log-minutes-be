from pyannote.audio import Pipeline
import os
from pyannote.core import Annotation


def diarize_audio(audio_file: str) -> Annotation:
    try:
        hf_auth_token = os.getenv("HF_AUTH_TOKEN")
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.0", use_auth_token = hf_auth_token)
        print(f"Audio_file: {audio_file}")
        diarization = pipeline(audio_file)
        return diarization
    except Exception as e:
        print(f"Error diarization:{e}")
    


