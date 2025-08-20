from pdfProcessing import censor_areas

def censor_names(names, clusters, word_data_enriched, input_pdf, output_pdf):
    """
    Censor all occurrences of multiple names in a PDF.

    :param names: List of names to censor (keys in clusters)
    :param clusters: Dictionary containing named entity clusters
    :param word_data_enriched: List of page data with words and coordinates
    :param input_pdf: Path to input PDF
    :param output_pdf: Path to output PDF
    """
    boxes = []

    for name in names:
        if name not in clusters:
            #print(f"Name '{name}' not found in clusters.")
            continue

        for mention in clusters[name]:
            page = mention['page']
            start_char = mention['start_char']
            end_char = mention['end_char']

            for page_data in word_data_enriched:
                if page_data["page"] != page:
                    continue

                for word in page_data["words"]:
                    # Check if the word overlaps with the target span
                    if not (word["char_no_in_text_latin_end"] < start_char or
                            word["char_no_in_text_latin_start"] > end_char):
                        x0, y0, x1, y1 = word["bbox"]
                        boxes.append((page, x0, y0, x1, y1))

    if boxes:
        censor_areas(input_pdf, output_pdf, boxes)
    else:
        print("No matching names found to censor.")
