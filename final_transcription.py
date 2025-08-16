import os

# === Folders ===
diar_folder = "diarizations"
trans_folder = "transcriptions_txt"
output_folder = "final_conversations"
os.makedirs(output_folder, exist_ok=True)

# === Function to parse diarization file ===
def read_diarization(file_path):
    diar_data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "]" in line:
                time_part, speaker = line.strip().split("] ")
                start, end = time_part.strip("[]").split(" - ")
                diar_data.append({
                    "start": float(start.strip("s")),
                    "end": float(end.strip("s")),
                    "speaker": speaker
                })
    return diar_data

# === Function to parse transcription file ===
def read_transcription(file_path):
    trans_data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "]" in line:
                try:
                    time_part, text = line.strip().split("] ", 1)
                except ValueError:
                    continue  # skip bad lines
                start, end = time_part.strip("[]").split(" - ")
                trans_data.append({
                    "start": float(start.strip("s")),
                    "end": float(end.strip("s")),
                    "text": text
                })
    return trans_data

# === Match diarization with transcription ===
def merge_diar_trans(diar_data, trans_data):
    merged = []
    for t in trans_data:
        for d in diar_data:
            if t["start"] >= d["start"] and t["end"] <= d["end"]:
                merged.append(f"[{d['speaker']}] {t['text']}")
                break
    return merged

# === Process each diarization file ===
for diar_file in os.listdir(diar_folder):
    if not diar_file.endswith(".txt"):
        continue

    # Looser matching: just take chunk number
    chunk_id = "".join([c for c in diar_file if c.isdigit()])
    trans_file = None
    for tf in os.listdir(trans_folder):
        if chunk_id and chunk_id in tf:
            trans_file = tf
            break

    if not trans_file:
        print(f"⚠️ No transcription found for {diar_file}")
        continue

    diar_path = os.path.join(diar_folder, diar_file)
    trans_path = os.path.join(trans_folder, trans_file)

    diar_data = read_diarization(diar_path)
    trans_data = read_transcription(trans_path)

    merged_convo = merge_diar_trans(diar_data, trans_data)

    output_path = os.path.join(output_folder, f"{chunk_id}_conversation.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_convo))

    print(f"✅ Merged conversation saved: {output_path}")
