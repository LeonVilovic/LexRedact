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
from entityGrouping import *

pdf_file = "sample.pdf"
word_data = extract_text_words_from_pdf(pdf_file)

# Convert back to plain text
plain_text = structured_data_to_text(word_data)

word_data_enriched = enrich_structured_data(word_data)

# Download Serbian models (only first time)
# This downloads all processors, including NER
#classla.download("sr")

# Load Serbian pipeline
nlp = classla.Pipeline("sr")

all_entities = []  # will store all entities across pages

for page in word_data_enriched:
    print(f"\n--- Page {page['page']} ---")
    doc = nlp(page["text_latin"])

    if doc.ents:
        for ent in doc.ents:
            if ent.type == 'PER':
                entity = {
                    "page": page["page"],
                    "text": ent.text,
                    "type": ent.type,
                    "start_char": ent.start_char,
                    "end_char": ent.end_char
                }
                print(f"{entity['text']} ({entity['type']}) [{entity['start_char']}:{entity['end_char']}]")
                all_entities.append(entity)
    else:
        print("No named entities found.")

# Now you can use all_entities
print("\n=== All entities collected ===")
for e in all_entities:
    print(e)

clusters = group_entities_fuzz_logic(all_entities, threshold=85)
print(clusters)

'''
# Optionally save structured data
with open("output_words.json", "w", encoding="utf-8") as f:
    json.dump(word_data, f, ensure_ascii=False, indent=2)
with open("output_words_enriched.json", "w", encoding="utf-8") as f:
    json.dump(word_data_enriched, f, ensure_ascii=False, indent=2)

# Optionally save text
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(plain_text)
'''
output_pdf = "censored.pdf"
#censor_every_second_word_replace_with_xxx(pdf_file, output_pdf, word_data)
censor_area(pdf_file, output_pdf, 2, 433.200008884553, 145.91999873021814, 476.64000977546937, 151.4399986821836)
print(f"Censored PDF saved as {output_pdf}")