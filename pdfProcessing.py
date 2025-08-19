import pymupdf
#import fitz as pymupdf
from PIL import Image
import io
import pytesseract

def extract_text_words_from_pdf(file_path):
    structured_data = []

    with pymupdf.open(file_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            words = page.get_text("words")
            page_words = []

            if not words:  # No text layer → use OCR
                print(f"Page {page_num}: No text layer found, running OCR...")

                # Render page as image
                pix = page.get_pixmap(dpi=300)

                # Convert to PIL image
                img = Image.open(io.BytesIO(pix.tobytes("png")))

                # OCR with bounding boxes
                #ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                # OCR with bounding boxes and full layout info and Serbian cyrilic
                ocr_data = pytesseract.image_to_data(img, lang='srp', output_type=pytesseract.Output.DICT)

                # Group word indices by (block_num, line_num)
                block_line_words = {}
                for i in range(len(ocr_data["text"])):
                    text = ocr_data["text"][i].strip()
                    if not text:
                        continue
                    block_num = ocr_data["block_num"][i]
                    line_num = ocr_data["line_num"][i]
                    key = (block_num, line_num)
                    block_line_words.setdefault(key, []).append(i)

                # Assign word_no within each line
                for (block_num, line_num), indices in sorted(block_line_words.items()):
                    for word_idx_in_line, i in enumerate(indices, start=1):
                        x, y, w, h = (
                            ocr_data["left"][i],
                            ocr_data["top"][i],
                            ocr_data["width"][i],
                            ocr_data["height"][i],
                        )
                        # Convert pixel coordinates to PDF coordinates
                        rect = pymupdf.Rect(
                            x * page.rect.width / pix.width,
                            y * page.rect.height / pix.height,
                            (x + w) * page.rect.width / pix.width,
                            (y + h) * page.rect.height / pix.height,
                        )
                        page_words.append({
                            "page": page_num,
                            "block_no": block_num,
                            "line_no": line_num,
                            "word_no": word_idx_in_line,
                            "word": ocr_data["text"][i],
                            "bbox": (rect.x0, rect.y0, rect.x1, rect.y1)
                        })
            else:  # Normal PDF with selectable text
                for word_tuple in words:
                    x0, y0, x1, y1, word, block_no, line_no, word_no = word_tuple
                    page_words.append({
                        "page": page_num,
                        "block_no": block_no,
                        "line_no": line_no,
                        "word_no": word_no,
                        "word": word,
                        "bbox": (x0, y0, x1, y1)
                    })

            structured_data.append({
                "page": page_num,
                "words": page_words
            })

    return structured_data

def censor_every_second_word_replace_with_xxx(input_pdf, output_pdf, structured_data):
    doc = pymupdf.open(input_pdf)

    for page_data in structured_data:
        page_index = page_data["page"] - 1
        page = doc[page_index]

        for i, word_info in enumerate(page_data["words"]):
            if i % 2 == 1:  # every second word
                x0, y0, x1, y1 = word_info["bbox"]
                rect = pymupdf.Rect(x0, y0, x1, y1)
                page.add_redact_annot(rect, fill=(0, 0, 0))  # black fill

        page.apply_redactions()

        for i, word_info in enumerate(page_data["words"]):
            if i % 2 == 1:
                x0, y0, x1, y1 = word_info["bbox"]
                rect = pymupdf.Rect(x0, y0, x1, y1)

                original_word = word_info["word"]
                replacement_text = "x" * len(original_word)

                fontsize = rect.height * 0.8
                text_width = fontsize * 0.6 * len(replacement_text)

                x_text = rect.x0 + (rect.width - text_width) / 2

                y_text = rect.y0 + rect.height * 0.80
                #y_text = rect.y0 + rect.height * 0.0  # baseline at bottom of bbox
                #y_text = rect.y0 + fontsize * 0.3  # 0.3 factor often works better for baseline

                page.insert_text(
                    (x_text, y_text),
                    replacement_text,
                    fontsize=fontsize,
                    fontname="helv",
                    color=(0, 0, 0),  # black text on black box
                )

    doc.save(output_pdf)
    doc.close()

def censor_area(input_pdf, output_pdf, page_number, x0, y0, x1, y1):
    """
    Parameters:
        input_pdf (str): Path to the input PDF
        output_pdf (str): Path to save the censored PDF
        page_number (int): Page number (1-based index)
        x0, y0, x1, y1 (float): Coordinates of the rectangle (bounding box)
    """
    doc = pymupdf.open(input_pdf)
    # Select the page (convert to 0-based index)
    page = doc[page_number - 1]
    rect = pymupdf.Rect(x0, y0, x1, y1)
    page.add_redact_annot(rect, fill=(0, 0, 0))
    page.apply_redactions()
    doc.save(output_pdf)
    doc.close()