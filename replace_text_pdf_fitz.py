import fitz  # import PyMuPDF

font_map = {
    "Arial": "helv",
    "ArialMT": "helv",
    "TimesNewRoman": "times",
    # add more as needed
}

doc = fitz.open("ok_org_sensitised.pdf")
page = doc[0]  # page number 0-based
# suppose you want to replace all occurrences of some text
disliked = "VAKUUTUSKIRJA"
better   = "Asiakasnumerot"
hits = page.search_for(disliked)  # list of rectangles where to replace

# Extract all spans with their bbox, font, and size
spans = []
for block in page.get_text("dict")["blocks"]:
    for line in block.get("lines", []):
        for s in line["spans"]:
            if s["text"].strip() == disliked:
                spans.append(s)

for rect in hits:
    matching_span = next(
        (s for s in spans if fitz.Rect(s["bbox"]).intersects(rect)), None
    )
    if matching_span:
        # Redact the original text (no padding)
        page.add_redact_annot(rect, fill=(1, 1, 1))  # white fill, no replacement text
page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

# Now insert the replacement text at the original position, with your desired size
for rect in hits:
    matching_span = next(
        (s for s in spans if fitz.Rect(s["bbox"]).intersects(rect)), None
    )
    if matching_span:
        fontname = font_map.get(matching_span.get("font", ""), "helv")
        y_baseline = matching_span["bbox"][1] + matching_span["size"]
        page.insert_text(
            (matching_span["bbox"][0], y_baseline),
            better,
            fontname=fontname,
            fontsize=matching_span.get("size", 11),
        )

doc.save("replaced.pdf", garbage=3, deflate=True)