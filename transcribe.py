import os, torch
from transformers import pipeline

# intial model to use
MODEL = "jacktol/whisper-medium.en-fine-tuned-for-ATC"
INPUT_FOLDER = "recordings-atc"
OUTPUT_FOLDER = "transcripts"
# short list of words we expect to hear, helps it pick the right names
PROMPT = "Kennedy Tower, New York Departure, Delta, American, JetBlue, Endeavor, runway three one left, line up and wait, cleared to land."

def main():
    # mps runs the model on the GPU, else use cpu
    if torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    print("using", device)
    # this part takes a while, load model once
    pipe = pipeline("automatic-speech-recognition", model=MODEL, device=device, torch_dtype=torch.float16)
    # the model wants the prompt as token ids, not plain text
    prompt_ids = pipe.tokenizer.get_prompt_ids(PROMPT, return_tensors="pt").to(device)

    # one folder per model so it can be compared later
    model_name = MODEL.split("/")[-1]
    out_dir = os.path.join(OUTPUT_FOLDER, model_name + "-prompt")
    os.makedirs(out_dir, exist_ok=True)

    for filename in sorted(os.listdir(INPUT_FOLDER)):
        if not filename.lower().endswith(".wav"):
            continue

        path = os.path.join(INPUT_FOLDER, filename)

        # same name as the audio file but .txt, skip if it's already done
        out_name = os.path.splitext(filename)[0] + ".txt"
        out_path = os.path.join(out_dir, out_name)
        if os.path.exists(out_path):
            continue

        print("transcribing", filename)

        # try to transcribe audio, catch errors
        try:
            # feed the audio into model in 30 second slices so it handles longer files
            result = pipe(path, chunk_length_s=30, generate_kwargs={"num_beams": 1, "prompt_ids": prompt_ids})
        except Exception as e:
            print("failed on", filename, "-", e)
            continue

        text = result["text"].strip()
        print(text)

        # save the text with the same name as the audio file
        with open(out_path, "w") as f:
            f.write(text)


if __name__ == "__main__":
    main()