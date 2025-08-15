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