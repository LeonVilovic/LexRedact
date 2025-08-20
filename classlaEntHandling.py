# pip install classla
import classla

def return_all_ents(word_data_enriched):

# Load Serbian pipeline
    nlp = classla.Pipeline("sr")

    all_entities = []

    for page in word_data_enriched:
        #print(f"\n--- Page {page['page']} ---")
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
                    #print(f"{entity['text']} ({entity['type']}) [{entity['start_char']}:{entity['end_char']}]")
                    all_entities.append(entity)
        else:
            print("No named entities found.")
    return all_entities

def download_serbian_models():

# Download Serbian models (only first time)
# This downloads all processors, including NER
    classla.download("sr")