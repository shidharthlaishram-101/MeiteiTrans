import sys
import io
from translator1 import translate

# Force UTF-8 output
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

if len(sys.argv) < 2:
    print("ERROR: No English text received.")
    sys.exit(1)

english_text = sys.argv[1]

result = translate(english_text)

print("TRANSLATION_RESULT_START")
print(result)
print("TRANSLATION_RESULT_END")