import transliterate
from transliterate import translit

def prepare_text_for_classla_pipeline(text):
    print("prepare_text_for_classla_pipeline step")
    print(text)
    text = text_to_latin(text)
    print("prepare_text_for_classla_pipeline step")
    print(text)
    text = remove_newline(text)
    print("prepare_text_for_classla_pipeline step FINAL")
    print(text)
    return text

def remove_newline(text):
    return text.replace('\n', ' ')

def text_to_latin(text):
    latin_text = translit(text, 'sr', reversed=True)
    return latin_text
