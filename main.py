import json
from get_pdf_text import get_pdf_text
from get_sensitive_data import get_sensitive_data
from assign_new_values import assign_new_value_with_llm
from swap_text_pdf import create_pdfs

PDF_PATH = "ok_org.pdf"

def main():
    text = get_pdf_text(PDF_PATH)
    sensitive_data_json = get_sensitive_data(text)
    sensitive_data = json.loads(sensitive_data_json)
    old_values = [item for value in sensitive_data.values() if value and value is not None for item in (value if isinstance(value, list) else [value])]
    new_values = [assign_new_value_with_llm(value) for value in old_values]
    create_pdfs(PDF_PATH, old_values, new_values)

if __name__ == "__main__":
    main()