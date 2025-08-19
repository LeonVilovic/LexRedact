import pymupdf  # PyMuPDF
from pdf2image import convert_from_path

import os
import json
import shutil
import re
from collections import defaultdict

from pdfProcessing import *
from structuredDataToText import *
from entityGrouping import *
from classlaEntHandling import *

pdf_file = "sample.pdf"
word_data = extract_text_words_from_pdf(pdf_file)

plain_text = structured_data_to_text(word_data)

word_data_enriched = enrich_structured_data(word_data)

all_entities = return_all_ents(word_data_enriched)

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