from pydub import AudioSegment
from pyannote.core import Annotation
import re
from datetime import datetime

def time_to_seconds(time: str) -> float:
    try:
        time =  datetime.strptime(time, "%H:%M:%S.%f")
        return time.hour * 3600 + time.minute * 60 + time.second + time.microsecond / 1e6
    except Exception as e:
        print(f"Error convert time: {e}")

def trim_audio(audio_file_path: str,
                start_time: int,
                end_time: int)->str:
    
    try:
        audio = AudioSegment.from_wav(audio_file_path)
        start_time_ms = time_to_seconds(start_time) * 1000
        end_time_ms = time_to_seconds(end_time) * 1000

        trimmed_audio = audio[start_time_ms: end_time_ms]
        output_file_path = f"{audio_file_path}_trimmed.wav"
        trimmed_audio.export(output_file_path, format="wav")

        print(f"Trimmed audio saved to: {output_file_path}")
        return output_file_path
    except Exception as e:
        print(f"Error Trim: {e}")

def format_diarization_result(diarization_result: Annotation) -> list:
    try:
        results = []
        cleaned_result = str(diarization_result).replace("[","").replace("]","").replace("-->","")
        pattern = r"(\d{2}:\d{2}:\d{2}\.\d{3})\s+(\d{2}:\d{2}:\d{2}\.\d{3})\s+\w+\s+(SPEAKER_\d+)"
        matches = re.findall(pattern, cleaned_result)

        for start, end, speaker in matches:
            results.append({
                "start_time": time_to_seconds(start),
                "end_time": time_to_seconds(end),
                "speaker": speaker
            })
        return results

    except Exception as e:
        print(f"Error format: {e}")