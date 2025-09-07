import re
from collections import Counter
from math import sqrt

def split_sentences(text: str):
    text = re.sub(r"\s+", " ", text).strip()
    return re.split(r"(?<=[.!?])\s+", text) if text else []

def tokenize(text: str):
    return re.findall(r"[A-Za-z0-9']+", text.lower())

def summarize_extractive(text: str, max_sentences: int = 3):
    sentences = split_sentences(text)
    if not sentences:
        return ""
    words = tokenize(text)
    freq = Counter(w for w in words if len(w) > 2)
    if not freq:
        return " ".join(sentences[:max_sentences])
    maxf = max(freq.values())
    if maxf == 0:
        return " ".join(sentences[:max_sentences])
    for w in list(freq):
        freq[w] /= maxf

    def sentence_score(s):
        tokens = tokenize(s)
        if not tokens:
            return 0.0
        score = sum(freq.get(t, 0.0) for t in tokens)
        return score / sqrt(len(tokens))

    ranked = sorted(((i, s, sentence_score(s)) for i, s in enumerate(sentences)),
                    key=lambda x: x[2], reverse=True)
    top = sorted(ranked[:max_sentences], key=lambda x: x[0])
    return " ".join(s for _, s, _ in top)

if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()
    summary = summarize_extractive(text, max_sentences=3)
    print(summary)