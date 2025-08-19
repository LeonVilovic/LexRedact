def prepare_text_for_classla_pipeline(text):
    print("prepare_text_for_classla_pipeline step1")
    print(text)
    text = remove_newline(text)
    print("prepare_text_for_classla_pipeline step FINAL")
    print(text)
    return text

def remove_newline(text):
    return text.replace('\n', ' ')

