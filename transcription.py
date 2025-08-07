import os
from groq import Groq
from dotenv import load_dotenv

# === Load API Key ===
load_dotenv()
api_key = os.getenv("WHISPHER_API_KEY")
client = Groq(api_key=api_key)

# === Input and Output Folders ===
input_folder = "audio_chunks"
txt_output_folder = "transcriptions_txt"
srt_output_folder = "transcriptions_srt"

os.makedirs(txt_output_folder, exist_ok=True)
os.makedirs(srt_output_folder, exist_ok=True)

# === Supported Formats ===
supported_extensions = [".wav", ".mp3", ".m4a"]

# === Time Formatter for .srt ===
def format_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# === Process Each Audio File ===
for file_name in os.listdir(input_folder):
    if not any(file_name.endswith(ext) for ext in supported_extensions):
        continue

    input_path = os.path.join(input_folder, file_name)
    base_name = os.path.splitext(file_name)[0]
    txt_output_path = os.path.join(txt_output_folder, f"{base_name}.txt")
    srt_output_path = os.path.join(srt_output_folder, f"{base_name}.srt")

    if os.path.exists(txt_output_path) and os.path.exists(srt_output_path):
        print(f"⏭️ Skipping {file_name} (already transcribed)")
        continue

    print(f"🔍 Transcribing: {file_name}...")

    # === Send to Groq Whisper ===
    with open(input_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=(file_name, audio_file.read()),
            model="whisper-large-v3",
            language="ur",
            response_format="verbose_json"
        )

    # === Save .txt Transcript ===
    with open(txt_output_path, "w", encoding="utf-8") as f_txt:
        for segment in transcription.segments:
            start = round(segment["start"], 2)
            end = round(segment["end"], 2)
            text = segment["text"].strip()
            f_txt.write(f"[{start}s - {end}s] {text}\n")

    # === Save .srt Subtitle ===
    with open(srt_output_path, "w", encoding="utf-8") as f_srt:
        for i, segment in enumerate(transcription.segments, start=1):
            start_time = format_srt_time(segment["start"])
            end_time = format_srt_time(segment["end"])
            text = segment["text"].strip()

            f_srt.write(f"{i}\n")
            f_srt.write(f"{start_time} --> {end_time}\n")
            f_srt.write(f"{text}\n\n")

    print(f"✅ Saved: {txt_output_path} and {srt_output_path}")
