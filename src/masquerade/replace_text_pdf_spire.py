from spire.pdf.common import *
from spire.pdf import *
import fitz  # PyMuPDF
import os

def remove_spire_watermark(file_path):
    temp_path = file_path + '.temp'
    os.rename(file_path, temp_path)
    doc = fitz.open(temp_path)
    unwanted = "Evaluation Warning : The document was created with Spire.PDF for Python."
    for page in doc:
        spans = page.get_text("dict")["blocks"]
        for block in spans:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if span["text"].strip() == unwanted:
                        rect = fitz.Rect(span["bbox"])
                        page.add_redact_annot(rect)
        page.apply_redactions()
    doc.save(file_path)
    doc.close()
    os.remove(temp_path)


def replace_text_pdf(input_path, output_path, old_texts, new_texts, highlight=False):
    doc = PdfDocument()
    doc.LoadFromFile(input_path)
    if highlight:
        color = Color.get_Red()
    else:
        color = Color.get_Black()
    for i in range(doc.Pages.Count):
        page = doc.Pages[i]
        replacer = PdfTextReplacer(page)
        for old_text, new_text in zip(old_texts, new_texts):
            replacer.ReplaceAllText(old_text, new_text, color)
    doc.SaveToFile(output_path)
    doc.Close()
    remove_spire_watermark(output_path)


def apply_highlights(input_path, output_path, texts):
    doc = PdfDocument()
    doc.LoadFromFile(input_path)
    for i in range(doc.Pages.Count):
        page = doc.Pages[i]
        finder = PdfTextFinder(page)
        for text in texts:
            results = finder.Find(text)
            for result in results:
                result.HighLight(Color.get_Yellow())
    doc.SaveToFile(output_path)
    doc.Close()
    remove_spire_watermark(output_path)


def create_pdfs(file_path, old_texts, new_texts):
    file_basename = os.path.splitext(os.path.basename(file_path))[0]
    highlighted_path = f"{file_basename}_highlighted.pdf"
    highlighted_masked_path = f"{file_basename}_highlighted_masked.pdf"
    masked_path = f"{file_basename}_masked.pdf"
    apply_highlights(file_path, highlighted_path, old_texts)
    replace_text_pdf(highlighted_path, highlighted_masked_path, old_texts, new_texts, True)
    replace_text_pdf(file_path, masked_path, old_texts, new_texts)
    os.remove(highlighted_path)


def main():
    file_path = "test.pdf"
    old_texts = ["Koulukatu 4", "Mikko Seppälä"]
    new_texts = ["Kurssitie 32", "Jari Kivi"]
    create_pdfs(file_path, old_texts, new_texts)


if __name__ == "__main__":
    main()
