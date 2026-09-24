import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import subprocess
import sys
import os

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_FILE = os.path.join(BASE_DIR, "english_input.wav")
TRANSLATOR_SCRIPT = os.path.join(BASE_DIR, "translate_once.py")
TTS_SCRIPT = os.path.join(BASE_DIR, "meitei_tts_generate.py")
OUTPUT_FILE = os.path.join(BASE_DIR, "translated_meitei.wav")

SAMPLE_RATE = 16000
RECORD_SECONDS = 8
MIC_DEVICE = 1

# --------------------------------------------------
# HEADER
# --------------------------------------------------

print("=" * 60)
print("ENGLISH VOICE -> MEITEI VOICE")
print("=" * 60)

# --------------------------------------------------
# STEP 1: RECORD ENGLISH
# --------------------------------------------------

print("\nMicrophone: AB13X USB Audio")
print(f"Recording for {RECORD_SECONDS} seconds...")
print("Please speak English now...\n")

try:
    recording = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
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

    print("Recording complete.")
    print("Audio saved:", AUDIO_FILE)

except Exception as e:
    print("\nRecording error:")
    print(type(e).__name__)
    print(e)
    sys.exit(1)

# --------------------------------------------------
# STEP 2: ENGLISH SPEECH -> ENGLISH TEXT
# --------------------------------------------------

recognizer = sr.Recognizer()

try:
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = recognizer.record(source)

    print("\nRecognizing English speech...")

    speech_text = recognizer.recognize_google(audio)

    print("\nEnglish:")
    print(speech_text)

except sr.UnknownValueError:
    print("\nSorry, I could not understand the English speech.")
    sys.exit(1)

except sr.RequestError as e:
    print("\nGoogle Speech Recognition service error:")
    print(e)
    sys.exit(1)

except Exception as e:
    print("\nSpeech recognition error:")
    print(type(e).__name__)
    print(e)
    sys.exit(1)

# --------------------------------------------------
# STEP 3: ENGLISH -> MEITEI
# --------------------------------------------------

print("\nStarting English -> Meitei translation...")

translation_process = subprocess.run(
    [
        sys.executable,
        "-u",
        TRANSLATOR_SCRIPT,
        speech_text
    ],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace"
)

print("\n--- TRANSLATOR OUTPUT ---")
print(translation_process.stdout)

if translation_process.stderr:
    print("\n--- TRANSLATOR ERROR ---")
    print(translation_process.stderr)

if translation_process.returncode != 0:
    print("\nTranslation process failed.")
    print("Exit code:", translation_process.returncode)
    sys.exit(1)

translator_output = translation_process.stdout

# --------------------------------------------------
# GET TRANSLATION RESULT
# --------------------------------------------------

start_marker = "TRANSLATION_RESULT_START"
end_marker = "TRANSLATION_RESULT_END"

if start_marker not in translator_output:
    print("\nCould not find translation result.")
    sys.exit(1)

if end_marker not in translator_output:
    print("\nCould not find end of translation result.")
    sys.exit(1)

translated_text = translator_output.split(
    start_marker,
    1
)[1].split(
    end_marker,
    1
)[0].strip()

print("\nMeitei Mayek:")
print(translated_text)

# --------------------------------------------------
# STEP 4: MEITEI TTS
# --------------------------------------------------

print("\nStarting Meitei TTS...")
print("Please wait...\n")

tts_process = subprocess.run(
    [
        sys.executable,
        "-u",
        TTS_SCRIPT,
        translated_text
    ]
)

print("\nTTS exit code:", tts_process.returncode)

# --------------------------------------------------
# STEP 5: PLAY MEITEI AUDIO
# --------------------------------------------------

if tts_process.returncode == 0:

    if os.path.exists(OUTPUT_FILE):

        print("\n" + "=" * 60)
        print("COMPLETE!")
        print("=" * 60)
        print("English voice -> English text")
        print("English text -> Meitei text")
        print("Meitei text -> Meitei voice")
        print("\nPlaying Meitei speech...")

        os.startfile(OUTPUT_FILE)

    else:
        print("\nTTS completed but WAV file was not found.")

else:
    print("\nMeitei TTS process failed.")
