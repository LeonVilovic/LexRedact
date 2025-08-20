import pymupdf  # PyMuPDF
from pdf2image import convert_from_path

import os
import sys
import json
import shutil
import re
from collections import defaultdict

from pdfProcessing import *
from structuredDataToText import *
from entityGrouping import *
from classlaEntHandling import *
from calcNew import *

ascii_art_logo = r"""
 _                  _____            _               _   
| |                |  __ \          | |             | |  
| |      ___ __  __| |__) | ___   __| |  __ _   ___ | |_ 
| |     / _ \\ \/ /|  _  / / _ \ / _` | / _` | / __|| __|
| |____|  __/ >  < | | \ \|  __/| (_| || (_| || (__ | |_ 
|______|\___|/_/\_\|_|  \_\\___| \__,_| \__,_| \___| \__|
"""

# Print in red
print("\033[31m" + ascii_art_logo + "\033[0m")

#pdf_file = "sample.pdf"
pdf_file_path = input("Enter the PDF file path: ")

pdf_file_path = pdf_file_path.strip('"').strip("'")
# Check if file exists and is a PDF
if os.path.isfile(pdf_file_path) and pdf_file_path.lower().endswith(".pdf"):
    print("Valid PDF file:", pdf_file_path)
else:
    print("Invalid file path or not a PDF. Exiting program.")
    sys.exit()
word_data = extract_text_words_from_pdf(pdf_file_path)

#plain_text = structured_data_to_text(word_data)

word_data_enriched = enrich_structured_data(word_data)

all_entities = return_all_ents(word_data_enriched)

'''
print("\n=== All entities collected ===")
for e in all_entities:
    print(e)
'''

clusters = group_entities_fuzz_logic(all_entities, threshold=85)

print("\n=== Spisak fizičkih lica ===")
for i, name in enumerate(clusters.keys(), start=1):
    print(f"{i}) {name}")
user_input = input("Ukucajte brojeve lica koje želite da cenzurišete, odvojene zapetama: ")

selected_numbers = [int(num.strip()) for num in user_input.split(",")]
cluster_list = list(clusters.keys())
selected_names = [cluster_list[num - 1] for num in selected_numbers]
print("Izabrana fizičkih lica:", selected_names)

base_name = os.path.basename(pdf_file_path)
name, ext = os.path.splitext(base_name)
output_name = f"{name}_censored{ext}"
output_pdf = os.path.join(os.path.dirname(pdf_file_path), output_name)

censor_names(selected_names, clusters, word_data_enriched, pdf_file_path, output_pdf)

print(f"Censored PDF saved as {output_pdf}")


#with open("output_words.json", "w", encoding="utf-8") as f:
#    json.dump(word_data, f, ensure_ascii=False, indent=2)
#with open("output_words_enriched.json", "w", encoding="utf-8") as f:
#    json.dump(word_data_enriched, f, ensure_ascii=False, indent=2)
#with open("output.txt", "w", encoding="utf-8") as f:
#    f.write(plain_text)