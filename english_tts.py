import sys
import pyttsx3
import os

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "translated_english.wav"
)

# --------------------------------------------------
# GET ENGLISH TEXT
# --------------------------------------------------

if len(sys.argv) < 2:
    print("ERROR: No English text received.")
    sys.exit(1)

text = " ".join(sys.argv[1:])

print("English text:")
print(text)

# --------------------------------------------------
# INITIALIZE TTS
# --------------------------------------------------

print("\nGenerating English speech...")

engine = pyttsx3.init()

# Speech speed
engine.setProperty("rate", 160)

# Volume
engine.setProperty("volume", 1.0)

# --------------------------------------------------
# GENERATE AUDIO
# --------------------------------------------------

engine.save_to_file(
    text,
    OUTPUT_FILE
)

engine.runAndWait()

# --------------------------------------------------
# CHECK OUTPUT
# --------------------------------------------------

if os.path.exists(OUTPUT_FILE):

    print("\nEnglish speech generated successfully!")
    print("Saved:", OUTPUT_FILE)

else:

    print("\nERROR: English audio file was not created.")
    sys.exit(1)