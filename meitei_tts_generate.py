import sys
import torch
import soundfile as sf
import os
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

# MODEL_ID = (
#     r"C:\Users\zuu17\.cache\huggingface\hub"
#     r"\models--naklitechie--indic-parler-tts"
#     r"\snapshots\dd37df3cadd8b7ec06c3ca5cc7c85fc5ea02b399"
# )

MODEL_ID = "naklitechie/indic-parler-tts"

# OUTPUT_FILE = r"D:\Voice TTS\translated_meitei.wav"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "translated_meitei.wav")

if len(sys.argv) < 2:
    print("No Meitei text received.")
    sys.exit(1)

text = sys.argv[1]

print("Loading Meitei TTS model...")

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)

model = ParlerTTSForConditionalGeneration.from_pretrained(
    MODEL_ID
).to(device)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

description = "A clear female voice speaking slowly and naturally."

print("Generating Meitei speech...")

description_inputs = tokenizer(
    description,
    return_tensors="pt"
).to(device)

prompt_inputs = tokenizer(
    text,
    return_tensors="pt"
).to(device)

with torch.no_grad():
    generation = model.generate(
        input_ids=description_inputs.input_ids,
        attention_mask=description_inputs.attention_mask,
        prompt_input_ids=prompt_inputs.input_ids,
        prompt_attention_mask=prompt_inputs.attention_mask
    )

audio = generation.cpu().numpy().squeeze()

sf.write(
    OUTPUT_FILE,
    audio,
    model.config.sampling_rate
)

print("Meitei speech generated successfully!")
print("Saved:", OUTPUT_FILE)