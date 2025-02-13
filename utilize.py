from pydub import AudioSegment


def time_to_seconds(time: str) -> int:
    try:
        h, m, s = time.split(':')
        return int(h)*3600 + int(m)*60 + int(s)
    except Exception as e:
        print(f"Error: {e}")

def trim_audio(audio_file_path: str,
                start_time: int,
                end_time: int, 
                output_file_path)->str:
    
    try:
        audio = AudioSegment.from_wav(audio_file_path)
        start_time = time_to_seconds(start_time)
        end_time = time_to_seconds(end_time)
        start_time_ms = start_time * 1000
        end_time_ms = end_time * 1000

        trimmed_audio = audio[start_time_ms, end_time_ms]
        trimmed_audio.export(output_file_path, format="wav")

        print(f"Trimmed audio saved to: {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")
