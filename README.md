# 🗣️ Speaker Diarization and Transcription in Urdu 🎙️🇵🇰

This project performs **speaker diarization** and **Urdu speech transcription** from long audio files (e.g., podcasts, interviews) using:

- 🧠 **pyannote-audio** (for speaker diarization)
- 🗣️ **Whisper via Groq API** (for Urdu transcription)
- 🧩 **Pydub** (for chunking long audio files)
- 💾 Text (.txt) and Subtitle (.srt) formatting for output

---

## ✅ Project Progress

### 🔹 1. Audio Preprocessing & Chunking
- ✅ Input: `.mp3`, `.wav`, `.m4a` long audio files
- ✅ Automatically splits audio into 3-minute chunks
- ✅ Converts to mono channel and 16kHz sampling rate
- ✅ Outputs clean `.wav` chunks in `audio_chunks/`

> 📂 Folder: `audio_chunks/`

---

### 🔹 2. Urdu Transcription (Using Groq + Whisper)
- ✅ Transcribes each chunk in Urdu using `whisper-large-v3`
- ✅ Language forced to `"ur"` for accuracy
- ✅ Transcription saved in:
  - ✅ `.txt` format (with timestamps)
  - ✅ `.srt` format (subtitles)

> 📂 Folders: `transcriptions_txt/`, `transcriptions_srt/`

---

### 🔹 3. Speaker Diarization (Using pyannote.audio)
- ✅ Loads HuggingFace `pyannote/speaker-diarization` model
- ✅ Processes each chunk to label `SPEAKER_00`, `SPEAKER_01`, etc.
- ✅ Time-aligned diarization segments

> 📂 Output coming soon: `diarization_segments/`

---

## 🛠️ Next Steps

- 🔄 Merge transcription + diarization into final format:
