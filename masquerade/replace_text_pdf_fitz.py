import fitz  # import PyMuPDF

font_map = {
    "Arial": "helv",
    "ArialMT": "helv",
    "TimesNewRoman": "times",
    # add more as needed
}

def replace_text(input_path, output_path, old_texts, new_texts):
    doc = fitz.open(input_path)

    for page in doc:
        # --- 1. Collect all redactions for all replacements ---
        all_spans = []
        for old_text, new_text in zip(old_texts, new_texts):
            hits = page.search_for(old_text)
            spans = []
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for s in line["spans"]:
                        if s["text"].strip() == old_text:
                            spans.append(s)
            for rect in hits:
                matching_span = next((s for s in spans if fitz.Rect(s["bbox"]).intersects(rect)), None)
                if matching_span:
                    page.add_redact_annot(rect, fill=(1, 1, 1))
                    all_spans.append((matching_span, new_text))
        # --- 2. Apply all redactions at once ---
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
        # --- 3. Insert all new texts ---
        for matching_span, new_text in all_spans:
            fontname = font_map.get(matching_span.get("font", ""), "helv")
            y_baseline = matching_span["bbox"][1] + matching_span["size"]
            page.insert_text(
                (matching_span["bbox"][0], y_baseline),
                new_text,
                fontname=fontname,
                fontsize=matching_span.get("size", 11),
            )

    doc.save(output_path, garbage=3, deflate=True)


if __name__ == "__main__":
    file_path = "test.pdf"
    old_texts = ["Koulukatu 4", "Mikko Seppälä"]
    new_texts = ["Kurssitie 32", "Jari Kivi"]
    replace_text(file_path, "replaced.pdf", old_texts, new_texts)