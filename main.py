from IOFunctions import *
from pdfProcessing import *
from structuredDataToText import *
from entityGrouping import *
from classlaEntHandling import *
from calcNew import *

print_logo()

print_disclamer()

pdf_file_path = let_user_input_pdf_file_path()

word_data = extract_text_words_from_pdf(pdf_file_path)

word_data_enriched = enrich_structured_data(word_data)

#call download_serbian_models() just the first time
#download_serbian_models()
all_entities = return_all_ents(word_data_enriched)

name_clusters = group_entities_fuzz_logic(all_entities, threshold=85)

selected_names = let_user_filter_names(name_clusters)

base_name = os.path.basename(pdf_file_path)
name, ext = os.path.splitext(base_name)
output_name = f"{name}_censored{ext}"
output_pdf = os.path.join(os.path.dirname(pdf_file_path), output_name)

censor_names(selected_names, name_clusters, word_data_enriched, pdf_file_path, output_pdf)

print(f"Censored PDF saved as {output_pdf}")

#with open("output_words.json", "w", encoding="utf-8") as f:
#    json.dump(word_data, f, ensure_ascii=False, indent=2)
#with open("output_words_enriched.json", "w", encoding="utf-8") as f:
#    json.dump(word_data_enriched, f, ensure_ascii=False, indent=2)
#with open("output.txt", "w", encoding="utf-8") as f:
#    f.write(plain_text)