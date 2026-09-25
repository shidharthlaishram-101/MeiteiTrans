import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000
RECORD_SECONDS = 8
MIC_DEVICE = 1

print("Recording Meitei speech...")
print("Speak now...")

recording = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    device=MIC_DEVICE
)

sd.wait()

sf.write(
    "meitei_input.wav",
    recording,
    SAMPLE_RATE
)

print("Saved: meitei_input.wav")