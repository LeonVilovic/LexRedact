def structured_data_to_text(structured_data):
    text_output = ""

    for page in structured_data:
        # Sort words by block, line, and word number
        sorted_words = sorted(
            page["words"],
            key=lambda w: (w["block_no"], w["line_no"], w["word_no"])
        )

        current_block = None
        current_line = None
        line_words = []

        for word_info in sorted_words:
            block_no = word_info["block_no"]
            line_no = word_info["line_no"]
            word = word_info["word"]

            # If we moved to a new line
            if (block_no != current_block) or (line_no != current_line):
                if line_words:
                    text_output += " ".join(line_words) + "\n"
                line_words = []
                current_block = block_no
                current_line = line_no

            line_words.append(word)

        # Add last line in the page
        if line_words:
            text_output += " ".join(line_words) + "\n"

        text_output += "\n"  # Page break

    return text_output.strip()

def enrich_structured_data_old(structured_data):
    enriched_pages = []

    for page in structured_data:
        # Sort words so we get proper text order
        sorted_words = sorted(
            page["words"],
            key=lambda w: (w["block_no"], w["line_no"], w["word_no"])
        )

        text_output = ""
        current_block = None
        current_line = None
        line_words = []
        char_pos = 0  # running character position in text

        # We'll build enriched words with char positions
        enriched_words = []

        for word_info in sorted_words:
            block_no = word_info["block_no"]
            line_no = word_info["line_no"]
            word = word_info["word"]

            # If new line/block starts → flush current line
            if (block_no != current_block) or (line_no != current_line):
                if line_words:
                    # Join words into line with spaces
                    line_text = " ".join(line_words)
                    text_output += line_text + "\n"
                    char_pos = len(text_output)  # update position after line break
                line_words = []
                current_block = block_no
                current_line = line_no

            # record char positions for this word
            start = char_pos + sum(len(w) + 1 for w in line_words)  # +1 for spaces
            end = start + len(word)

            enriched_word = dict(word_info)  # copy original dict
            enriched_word["char_no_in_text_start"] = start
            enriched_word["char_no_in_text_end"] = end
            enriched_words.append(enriched_word)

            line_words.append(word)

        # flush last line of page
        if line_words:
            line_text = " ".join(line_words)
            text_output += line_text + "\n"

        enriched_pages.append({
            "page": page["page"],
            "text": text_output.strip(),
            "words": enriched_words
        })

    return enriched_pages

# Basic Serbian Cyrillic → Latin transliteration map
CYR_TO_LAT_MAP = {
    "А": "A", "а": "a",
    "Б": "B", "б": "b",
    "В": "V", "в": "v",
    "Г": "G", "г": "g",
    "Д": "D", "д": "d",
    "Ђ": "Đ", "ђ": "đ",
    "Е": "E", "е": "e",
    "Ж": "Ž", "ж": "ž",
    "З": "Z", "з": "z",
    "И": "I", "и": "i",
    "Ј": "J", "ј": "j",
    "К": "K", "к": "k",
    "Л": "L", "л": "l",
    "Љ": "Lj", "љ": "lj",
    "М": "M", "м": "m",
    "Н": "N", "н": "n",
    "Њ": "Nj", "њ": "nj",
    "О": "O", "о": "o",
    "П": "P", "п": "p",
    "Р": "R", "р": "r",
    "С": "S", "с": "s",
    "Т": "T", "т": "t",
    "Ћ": "Ć", "ћ": "ć",
    "У": "U", "у": "u",
    "Ф": "F", "ф": "f",
    "Х": "H", "х": "h",
    "Ц": "C", "ц": "c",
    "Ч": "Č", "ч": "č",
    "Џ": "Dž", "џ": "dž",
    "Ш": "Š", "ш": "š",
}

def cyr_to_lat(text: str) -> str:
    """Convert Cyrillic string to Latin."""
    return "".join(CYR_TO_LAT_MAP.get(ch, ch) for ch in text)


def enrich_structured_data(structured_data):
    enriched_pages = []

    for page in structured_data:
        # Sort words for proper text order
        sorted_words = sorted(
            page["words"],
            key=lambda w: (w["block_no"], w["line_no"], w["word_no"])
        )

        text_output_cyr = ""
        text_output_lat = ""
        current_block = None
        current_line = None
        line_words_cyr = []
        line_words_lat = []

        char_pos_cyr = 0
        char_pos_lat = 0

        enriched_words = []

        for word_info in sorted_words:
            block_no = word_info["block_no"]
            line_no = word_info["line_no"]
            word_cyr = word_info["word"]
            word_lat = cyr_to_lat(word_cyr)

            # If we moved to a new line
            if (block_no != current_block) or (line_no != current_line):
                if line_words_cyr:
                    line_text_cyr = " ".join(line_words_cyr)
                    line_text_lat = " ".join(line_words_lat)
                    text_output_cyr += line_text_cyr + "\n"
                    text_output_lat += line_text_lat + "\n"
                    char_pos_cyr = len(text_output_cyr)
                    char_pos_lat = len(text_output_lat)

                line_words_cyr = []
                line_words_lat = []
                current_block = block_no
                current_line = line_no

            # Compute Cyrillic positions
            start_cyr = char_pos_cyr + sum(len(w) + 1 for w in line_words_cyr)
            end_cyr = start_cyr + len(word_cyr)

            # Compute Latin positions
            start_lat = char_pos_lat + sum(len(w) + 1 for w in line_words_lat)
            end_lat = start_lat + len(word_lat)

            enriched_word = dict(word_info)
            enriched_word["char_no_in_text_start"] = start_cyr
            enriched_word["char_no_in_text_end"] = end_cyr
            enriched_word["char_no_in_text_latin_start"] = start_lat
            enriched_word["char_no_in_text_latin_end"] = end_lat

            enriched_words.append(enriched_word)

            line_words_cyr.append(word_cyr)
            line_words_lat.append(word_lat)

        # Flush last line
        if line_words_cyr:
            text_output_cyr += " ".join(line_words_cyr) + "\n"
            text_output_lat += " ".join(line_words_lat) + "\n"

        enriched_pages.append({
            "page": page["page"],
            #"text": text_output_cyr.strip(),
            "text": text_output_cyr.strip().replace('\n', ' '),
            #"text_latin": text_output_lat.strip().replace('\n', ' '),
            "text_latin": text_output_lat.strip().replace('\n', ' '),
            "words": enriched_words
        })

    return enriched_pages