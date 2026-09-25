import sounddevice as sd
import soundfile as sf
import subprocess
import sys
import os


# ==========================================================
# SETTINGS
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# Audio input
AUDIO_FILE = os.path.join(
    BASE_DIR,
    "meitei_input.wav"
)

# Output audio
OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "translated_english.wav"
)

# Scripts
STT_SCRIPT = os.path.join(
    BASE_DIR,
    "meitei_stt.py"
)

TRANSLATOR_SCRIPT = os.path.join(
    BASE_DIR,
    "meitei_to_english.py"
)

TTS_SCRIPT = os.path.join(
    BASE_DIR,
    "english_tts.py"
)

# Recording settings
SAMPLE_RATE = 16000
RECORD_SECONDS = 8

# Change this if your microphone has another device ID
MIC_DEVICE = 1


# ==========================================================
# HEADER
# ==========================================================

print()
print("=" * 65)
print("              MEITEI → ENGLISH VOICE TRANSLATOR")
print("=" * 65)
print()


# ==========================================================
# STEP 1 — RECORD MEITEI SPEECH
# ==========================================================

print("STEP 1/4 — Recording Meitei speech")
print("-" * 65)

print(f"Recording for {RECORD_SECONDS} seconds...")
print("Please speak Meitei now.")
print()

try:

    recording = sd.rec(
        int(
            RECORD_SECONDS *
            SAMPLE_RATE
        ),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=MIC_DEVICE
    )

    sd.wait()

    sf.write(
        AUDIO_FILE,
        recording,
        SAMPLE_RATE
    )

    print("✓ Recording complete.")
    print(f"✓ Saved: {AUDIO_FILE}")

except Exception as e:

    print()
    print("✗ Recording failed.")
    print(type(e).__name__)
    print(e)

    sys.exit(1)


# ==========================================================
# STEP 2 — MEITEI SPEECH → MEITEI TEXT
# ==========================================================

print()
print("STEP 2/4 — Meitei Speech → Meitei Text")
print("-" * 65)

try:

    stt_process = subprocess.run(
        [
            sys.executable,
            "-u",
            STT_SCRIPT,
            AUDIO_FILE
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

except Exception as e:

    print("✗ Could not start Meitei ASR.")
    print(e)
    sys.exit(1)


if stt_process.returncode != 0:

    print()
    print("✗ Meitei ASR failed.")

    if stt_process.stdout:
        print(stt_process.stdout)

    if stt_process.stderr:
        print(stt_process.stderr)

    sys.exit(1)


# ----------------------------------------------------------
# Extract ASR result
# ----------------------------------------------------------

start_marker = "ASR_RESULT_START"
end_marker = "ASR_RESULT_END"

if start_marker not in stt_process.stdout:

    print("✗ Could not find ASR result.")
    print(stt_process.stdout)

    sys.exit(1)

if end_marker not in stt_process.stdout:

    print("✗ Could not find ASR end marker.")
    print(stt_process.stdout)

    sys.exit(1)


meitei_text = (
    stt_process.stdout
    .split(start_marker, 1)[1]
    .split(end_marker, 1)[0]
    .strip()
)


if not meitei_text:

    print("✗ ASR returned empty text.")
    sys.exit(1)


print()
print("Meitei Text:")
print(meitei_text)


# ==========================================================
# STEP 3 — MEITEI TEXT → ENGLISH TEXT
# ==========================================================

print()
print("STEP 3/4 — Meitei Text → English Text")
print("-" * 65)

try:

    translation_process = subprocess.run(
        [
            sys.executable,
            "-u",
            TRANSLATOR_SCRIPT,
            meitei_text
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

except Exception as e:

    print("✗ Could not start translator.")
    print(e)

    sys.exit(1)


if translation_process.returncode != 0:

    print()
    print("✗ Translation failed.")

    if translation_process.stdout:
        print(translation_process.stdout)

    if translation_process.stderr:
        print(translation_process.stderr)

    sys.exit(1)


# ----------------------------------------------------------
# Extract translation result
# ----------------------------------------------------------

start_marker = "TRANSLATION_RESULT_START"
end_marker = "TRANSLATION_RESULT_END"

if start_marker not in translation_process.stdout:

    print("✗ Could not find translation result.")

    print(
        translation_process.stdout
    )

    sys.exit(1)

if end_marker not in translation_process.stdout:

    print("✗ Could not find translation end marker.")

    print(
        translation_process.stdout
    )

    sys.exit(1)


english_text = (
    translation_process.stdout
    .split(start_marker, 1)[1]
    .split(end_marker, 1)[0]
    .strip()
)


if not english_text:

    print("✗ Translator returned empty text.")
    sys.exit(1)


print()
print("English Text:")
print(english_text)


# ==========================================================
# STEP 4 — ENGLISH TEXT → ENGLISH SPEECH
# ==========================================================

print()
print("STEP 4/4 — English Text → English Speech")
print("-" * 65)

try:

    tts_process = subprocess.run(
        [
            sys.executable,
            "-u",
            TTS_SCRIPT,
            english_text
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

except Exception as e:

    print("✗ Could not start English TTS.")
    print(e)

    sys.exit(1)


if tts_process.returncode != 0:

    print()
    print("✗ English TTS failed.")

    if tts_process.stdout:
        print(tts_process.stdout)

    if tts_process.stderr:
        print(tts_process.stderr)

    sys.exit(1)


print(
    tts_process.stdout
)

if tts_process.stderr:

    print(
        tts_process.stderr
    )


# ==========================================================
# PLAY RESULT
# ==========================================================

print()
print("=" * 65)
print("                       COMPLETE")
print("=" * 65)

print()
print("Meitei Speech")
print("      ↓")
print("Meitei Text")
print("      ↓")
print("English Text")
print("      ↓")
print("English Speech")
print()

print("Meitei:")
print(meitei_text)

print()

print("English:")
print(english_text)

print()


if os.path.exists(OUTPUT_FILE):

    print("✓ English audio generated:")
    print(OUTPUT_FILE)

    print()
    print("Playing English speech...")

    try:
        os.startfile(OUTPUT_FILE)

    except Exception as e:

        print(
            "Could not automatically play audio:"
        )

        print(e)

else:

    print(
        "✗ English audio file was not found."
    )

    sys.exit(1)


print()
print("=" * 65)