import pymupdf  # PyMuPDF
from pdf2image import convert_from_path

import os
import json
import shutil
# pip install classla
import classla
import re
from collections import defaultdict

from pdfProcessing import *
from structuredDataToText import *
from textProcessing import *

pdf_file = "sample.pdf"
word_data = extract_text_words_from_pdf(pdf_file)

# Convert back to plain text
plain_text = structured_data_to_text(word_data)

# Download Serbian models (only first time)
# This downloads all processors, including NER
#classla.download("sr")

# Load Serbian pipeline
nlp = classla.Pipeline("sr")
# Process text
doc = nlp(prepare_text_for_classla_pipeline(plain_text))

# Extract noun phrases (approximation using NOUN/PROPN tags)
noun_phrases = [
    " ".join(w.text for w in sent.words if w.upos in ["NOUN", "PROPN"])
    for sent in doc.sentences
]
print("Noun phrases:", noun_phrases)

# Extract verbs
verbs = [w.lemma for sent in doc.sentences for w in sent.words if w.upos == "VERB"]
print("Verbs:", verbs)

# Named entities
print("Named entities:")
for ent in doc.ents:
    print(ent.text, ent.type, ent.start_char, ent.end_char)

# --- helpers ---
def deinflect_lastname(token: str) -> str:
    t = token

    # Strip common Serbian possessive forms first (e.g., "Thrunova" -> "Thrun")
    for suf in ("ova", "eva", "ina"):
        if t.lower().endswith(suf) and len(t) > len(suf) + 2:
            t = t[:-len(suf)]
            break

    # Strip possessive stems if present (e.g., "Thrunov" -> "Thrun")
    for suf in ("ov", "ev", "in"):
        if t.lower().endswith(suf) and len(t) > len(suf) + 2:
            t = t[:-len(suf)]
            break

    # Strip common case endings (gentle)
    for suf in ("om", "og", "u", "a", "e", "i"):
        if t.lower().endswith(suf) and len(t) > len(suf) + 2:
            t = t[:-len(suf)]
            break

    return t

def normalize_fullname(ent_text: str) -> str:
    # Normalize only the last token; keep original casing on the rest
    parts = ent_text.split()
    if not parts:
        return ent_text.strip()

    if len(parts) == 1:
        # single token (likely last name or given name)
        return deinflect_lastname(parts[0])

    last_base = deinflect_lastname(parts[-1])
    parts[-1] = last_base
    return " ".join(parts)

# --- build mapping from classla doc ---
people = []
for ent in doc.ents:
    if ent.type != "PER":
        continue
    text = ent.text.strip()
    norm_full = normalize_fullname(text)
    parts = norm_full.split()
    base_last = parts[-1] if parts else norm_full
    people.append({
        "orig": text,
        "norm_full": norm_full,         # e.g., "Sebastian Thrun" or "Thrun"
        "base_last_lc": base_last.lower(),
        "is_full": len(parts) >= 2,
        "start": ent.start_char,
    })

# 1) choose canonical full name per last name: earliest occurrence in text
canonical_full_by_last = {}  # last -> (start, canonical_full)
for p in people:
    if p["is_full"]:
        last = p["base_last_lc"]
        cand = p["norm_full"]
        if last not in canonical_full_by_last or p["start"] < canonical_full_by_last[last][0]:
            canonical_full_by_last[last] = (p["start"], cand)

# 2) build final variant -> canonical map
variant_to_canonical = {}
for p in people:
    last = p["base_last_lc"]
    # Prefer the earliest full-name for this last name, if it exists
    if last in canonical_full_by_last:
        canonical = canonical_full_by_last[last][1]
    else:
        # No known full name for this last: keep normalized form as canonical
        canonical = p["norm_full"]

    variant_to_canonical[p["orig"]] = canonical

# 3) also group into clusters by canonical
clusters = defaultdict(set)
for variant, canon in variant_to_canonical.items():
    clusters[canon].add(variant)

# --- demo prints ---
print("Variant → Canonical:")
for k, v in variant_to_canonical.items():
    print(f"{k!r} -> {v!r}")

print("\nClusters:")
for canon, vars_ in clusters.items():
    print(f"{canon!r}: {sorted(vars_)}")

# Optionally save structured data
with open("output_words.json", "w", encoding="utf-8") as f:
    json.dump(word_data, f, ensure_ascii=False, indent=2)

# Optionally save text
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(plain_text)

output_pdf = "censored.pdf"
censor_every_second_word_replace_with_xxx(pdf_file, output_pdf, word_data)

print(f"Censored PDF saved as {output_pdf}")