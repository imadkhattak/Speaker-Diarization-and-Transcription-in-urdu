from pydub import AudioSegment
import os


input_path = "/audios/mooroo-podcast-48-engineer-muhammad-ali-mirza_RuDs7kOP.mp3"
output_dir = "audio_chunks"
chunk_length_ms = 3 * 60 * 1000  


audio = AudioSegment.from_file(input_path)
total_duration_ms = len(audio)


os.makedirs(output_dir, exist_ok=True)

for i in range(0, total_duration_ms, chunk_length_ms):
    chunk = audio[i:i + chunk_length_ms]
    chunk = chunk.set_channels(1).set_frame_rate(16000)
    chunk_name = os.path.join(output_dir, f"chunk_{i//chunk_length_ms + 1}.wav")
    chunk.export(chunk_name, format="wav")
    print(f"✅ Exported {chunk_name}")
