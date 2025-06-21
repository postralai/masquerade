import fitz

def get_pdf_text(file_path, page_chunks=False):
    doc = fitz.open(file_path)
    cleaned = fitz.open()
    if page_chunks:
        texts = []
        for page in doc:
            page_text = ""
            new_page = cleaned.new_page(width=page.rect.width, height=page.rect.height)
            for span in page.get_text("dict")["blocks"]:
                for line in span.get("lines", []):
                    for s in line["spans"]:
                        page_text += s["text"] + "\n"
            texts.append(page_text)
        return texts
    else:
        text = ""
        for page in doc:
            new_page = cleaned.new_page(width=page.rect.width, height=page.rect.height)
            for span in page.get_text("dict")["blocks"]:
                for line in span.get("lines", []):
                    for s in line["spans"]:
                        text += s["text"] + "\n"
        return text

if __name__ == "__main__":
    text = get_pdf_text("ok_org_sensitised.pdf")
    print(text)