import os
from pyannote.audio import Pipeline
from dotenv import load_dotenv


load_dotenv()
hf_token = os.getenv("HUGGINGFACE_TOKEN")


pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=hf_token)

# === Input and Output Folders ===
input_folder = "audio_chunks"
output_folder = "diarizations"
os.makedirs(output_folder, exist_ok=True)


supported_extensions = [".wav"]


for file_name in os.listdir(input_folder):
    if not any(file_name.endswith(ext) for ext in supported_extensions):
        continue

    input_path = os.path.join(input_folder, file_name)
    base_name = os.path.splitext(file_name)[0]
    output_path = os.path.join(output_folder, f"{base_name}_diarization.txt")

    if os.path.exists(output_path):
        print(f"⏭️ Skipping {file_name} (already diarized)")
        continue

    print(f"🔍 Diarizing: {file_name}...")


    diarization = pipeline(input_path)


    with open(output_path, "w", encoding="utf-8") as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            f.write(f"[{turn.start:.2f}s - {turn.end:.2f}s] {speaker}\n")

    print(f"✅ Diarization saved: {output_path}")
