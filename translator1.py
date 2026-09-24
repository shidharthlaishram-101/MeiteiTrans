import os
import json
import numpy as np
import onnxruntime as ort
from huggingface_hub import snapshot_download
from tokenizers import Tokenizer


MODEL_ID = "hari31416/indictrans2-en-indic-dist-200M-ONNX-int8"

print("Loading Meitei translation model...")

MODEL_DIR = snapshot_download(MODEL_ID)

# ---------------------------------------------------------
# Load configuration
# ---------------------------------------------------------

with open(
    os.path.join(MODEL_DIR, "generation_config.json"),
    "r",
    encoding="utf-8"
) as f:
    generation_config = json.load(f)

decoder_start_id = int(
    generation_config.get("decoder_start_token_id", 2)
)

eos_id = int(
    generation_config.get("eos_token_id", 2)
)


# ---------------------------------------------------------
# Load tokenizers
# ---------------------------------------------------------

src_tokenizer = Tokenizer.from_file(
    os.path.join(MODEL_DIR, "tokenizer_src.json")
)

tgt_tokenizer = Tokenizer.from_file(
    os.path.join(MODEL_DIR, "tokenizer_tgt.json")
)

with open(
    os.path.join(MODEL_DIR, "tokenizer_meta.json"),
    "r",
    encoding="utf-8"
) as f:
    meta = json.load(f)


# ---------------------------------------------------------
# Load ONNX models
# ---------------------------------------------------------

encoder = ort.InferenceSession(
    os.path.join(MODEL_DIR, "encoder_model.onnx"),
    providers=["CPUExecutionProvider"]
)

decoder = ort.InferenceSession(
    os.path.join(MODEL_DIR, "decoder_model.onnx"),
    providers=["CPUExecutionProvider"]
)

decoder_past = ort.InferenceSession(
    os.path.join(MODEL_DIR, "decoder_with_past_model.onnx"),
    providers=["CPUExecutionProvider"]
)

num_layers = (len(decoder.get_outputs()) - 1) // 4

print("Meitei translator loaded")


# ---------------------------------------------------------
# KV cache helper
# ---------------------------------------------------------

def build_past_inputs(past_outputs):

    inputs = {}

    decoder_inputs = decoder_past.get_inputs()

    past_input_names = [
        x.name
        for x in decoder_inputs
        if "past" in x.name.lower()
    ]

    for i, name in enumerate(past_input_names):

        if i < len(past_outputs):
            inputs[name] = past_outputs[i]

    return inputs


# ---------------------------------------------------------
# Translation function
# ---------------------------------------------------------

def translate(text, max_new_tokens=128):

    prefixed = f"eng_Latn mni_Mtei {text}"

    encoded = src_tokenizer.encode(prefixed)

    input_ids = np.array(
        [[
            token_id
            if token_id < meta["src_dict_size"]
            else meta["unk_id"]
            for token_id in encoded.ids
        ]],
        dtype=np.int64
    )

    attention_mask = np.array(
        [encoded.attention_mask],
        dtype=np.int64
    )

    # -----------------------------------------------------
    # Encoder
    # -----------------------------------------------------

    encoder_output = encoder.run(
        ["last_hidden_state"],
        {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }
    )[0]

    # -----------------------------------------------------
    # Decoder
    # -----------------------------------------------------

    decoder_input_ids = np.array(
        [[decoder_start_id]],
        dtype=np.int64
    )

    output_ids = [decoder_start_id]

    past_outputs = None

    for step in range(max_new_tokens):

        if step == 0:

            decoder_outputs = decoder.run(
                None,
                {
                    "input_ids": decoder_input_ids,
                    "encoder_hidden_states": encoder_output,
                    "encoder_attention_mask": attention_mask,
                }
            )

        else:

            decoder_outputs = decoder_past.run(
                None,
                {
                    "input_ids": decoder_input_ids,
                    "encoder_attention_mask": attention_mask,
                    **build_past_inputs(past_outputs),
                }
            )

        logits = decoder_outputs[0]

        past_outputs = list(decoder_outputs[1:])

        next_id = int(
            np.argmax(
                logits[0, -1, :]
            )
        )

        output_ids.append(next_id)

        if next_id == eos_id:
            break

        decoder_input_ids = np.array(
            [[next_id]],
            dtype=np.int64
        )

    # -----------------------------------------------------
    # Decode
    # -----------------------------------------------------

    safe_ids = [
        token_id
        if token_id < meta["tgt_dict_size"]
        else meta["unk_id"]
        for token_id in output_ids
    ]

    result = tgt_tokenizer.decode(
        safe_ids,
        skip_special_tokens=True
    )

    return result