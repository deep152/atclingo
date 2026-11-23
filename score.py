import os, re
import jiwer

REF_FOLDER = "recordings-atc"
OUT_FOLDER = "transcripts"

# spoken numbers -> digits so "three thirty six" and "336" match
ones = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "niner": 9}
teens = {"ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
         "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
tens = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}

def numbers_to_digits(text):
    words = text.split()
    out = []
    current = ""
    i = 0
    while i < len(words):
        w = words[i]
        if w in ones:
            current += str(ones[w])
        elif w in teens:
            current += str(teens[w])
        elif w in tens:
            # "thirty six" -> 36
            if i + 1 < len(words) and words[i + 1] in ones and ones[words[i + 1]] > 0:
                current += str(tens[w] + ones[words[i + 1]])
                i += 1
            else:
                current += str(tens[w])
        elif w == "thousand" and current:
            current += "000"
        elif w == "hundred" and current:
            current += "00"
        elif w == "point":
            current += "."
        elif re.fullmatch(r"\d+(\.\d+)?", w):
            current += w
        else:
            if current:
                out.append(current)
                current = ""
            out.append(w)
        i += 1
    if current:
        out.append(current)
    return " ".join(out)

def clean(text):
    text = text.lower()
    # drop the parts i couldn't hear
    text = re.sub(r"\[.*?\]", " ", text)
    # no punctuation (keep digits and dots for now)
    text = re.sub(r"[^a-z0-9. ]", " ", text)
    text = numbers_to_digits(text)
    # now the dots can go
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return " ".join(text.split())

for model in sorted(os.listdir(OUT_FOLDER)):
    model_dir = os.path.join(OUT_FOLDER, model)
    if not os.path.isdir(model_dir):
        continue
    print(model)
    scores = []
    for name in sorted(os.listdir(model_dir)):
        ref_path = os.path.join(REF_FOLDER, name)
        # skip old clips that have no hand transcript
        if not os.path.exists(ref_path):
            continue
        ref = clean(open(ref_path).read())
        hyp = clean(open(os.path.join(model_dir, name)).read())
        wer = jiwer.wer(ref, hyp)
        scores.append(wer)
        print("  ", name, round(wer * 100), "%")
    if scores:
        print("   average", round(sum(scores) / len(scores) * 100), "%")