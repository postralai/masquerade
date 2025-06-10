from get_pdf_text import get_pdf_text
from get_sensitive_data import get_sensitive_data
from assign_new_values import assign_new_value_with_llm
from swap_text_pdf import swap_text_pdf

PDF_PATH = "ok_org.pdf"

def main():
    text = get_pdf_text(PDF_PATH)
    sensitive_data_json = get_sensitive_data(text)
    sensitive_data = json.loads(sensitive_data_json)
    old_values = sensitive_data.values()
    new_values = [assign_new_value_with_llm(value) for value in original_values]
    swapped_text = swap_text_pdf(text, old_values, new_values)
    

if __name__ == "__main__":
    main()