import sys
import io
import onnx_asr


# ==========================================================
# FORCE UTF-8 OUTPUT
# ==========================================================

sys.stdout = io.TextIOWrapper(
    sys.stdout.buffer,
    encoding="utf-8",
    errors="replace"
)

sys.stderr = io.TextIOWrapper(
    sys.stderr.buffer,
    encoding="utf-8",
    errors="replace"
)


# ==========================================================
# MODEL
# ==========================================================

MODEL_ID = "OpenVoiceOS/ai4bharat-indicconformer-mni-onnx"

print("Loading Meitei ASR model...")

model = onnx_asr.load_model(
    MODEL_ID,
    quantization="int8"
)

print("Meitei ASR loaded.")


# ==========================================================
# TRANSCRIPTION
# ==========================================================

def transcribe(audio_file):

    result = model.recognize(
        audio_file
    )

    return result


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "ERROR: No audio file received."
        )

        sys.exit(1)

    audio_file = sys.argv[1]

    print(
        "Recognizing:",
        audio_file
    )

    try:

        text = transcribe(
            audio_file
        )

        print(
            "ASR_RESULT_START"
        )

        print(text)

        print(
            "ASR_RESULT_END"
        )

    except Exception as e:

        print(
            "ASR_ERROR_START"
        )

        print(
            type(e).__name__
        )

        print(
            str(e)
        )

        print(
            "ASR_ERROR_END"
        )

        sys.exit(1)