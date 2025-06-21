import fitz

# Make consistent font but removes images
doc = fitz.open("ok_org_sensitised.pdf")
cleaned = fitz.open()

for page in doc:
    new_page = cleaned.new_page(width=page.rect.width, height=page.rect.height)
    for span in page.get_text("dict")["blocks"]:
        for line in span.get("lines", []):
            for s in line["spans"]:
                print(s["text"])
                if s["text"].strip() == "Evaluation Warning : The document was created with Spire.PDF for Python.":
                    continue
                new_page.insert_text((s["bbox"][0], s["bbox"][1]), s["text"], fontsize=s["size"])
                
cleaned.save("cleaned_output.pdf")
