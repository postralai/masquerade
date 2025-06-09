from spire.pdf.common import *
from spire.pdf import *

def swap_text_pdf(input_path, output_path, old_texts, new_texts):
    doc = PdfDocument()
    doc.LoadFromFile(input_path)

    # Iterate through the pages in the document
    for i in range(doc.Pages.Count):
        # Get the current page
        page = doc.Pages[i]    
        # Create an object of the PdfTextReplace class and pass the page to the constructor of the class as a parameter
        replacer = PdfTextReplacer(page)
        
        # Replace All instances of a specific text with new text
        for old_text, new_text in zip(old_texts, new_texts):
            replacer.ReplaceAllText(old_text, new_text, Color.get_Blue())

    # Save the resulting file
    doc.SaveToFile(output_path)
    doc.Close()

old_texts = ["74503310", "24-00049-92853-4", "0303 0303", "Kuljetus Luokkanen Oy", "Parsipolku 8", "93100 PUDASJÄRVI"]
new_texts = ["09834058", "32-34535-34542-3", "0213 0225", "Kuljetus Testeri Oy", "Koulupolku 8", "05938 JOUTJÄRVI"]
swap_text_pdf("ok_org.pdf", "ok_new.pdf", old_texts, new_texts)
