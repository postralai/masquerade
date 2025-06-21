from masquerade.get_pdf_text import get_pdf_text
from masquerade.get_sensitive_data import get_sensitive_data, post_process_sensitive_data
from masquerade.assign_new_values import assign_new_value_with_llm
from masquerade.replace_text_pdf_spire import create_pdfs
from masquerade.tinfoil_llm import TinfoilLLM

PDF_PATH = "insurance_offer.pdf"

def assign_new_values(old_values, tinfoil_llm):
    new_values = []
    for value in old_values:
        if value is not None:
            try:
                new_value = assign_new_value_with_llm(value, tinfoil_llm)
                new_values.append(new_value)
            except Exception as e:
                print(f"Error processing value '{value}': {str(e)}")
                continue
    return new_values

def print_mapping_table(old_values, new_values):
    print("\nValue Mappings:")
    print("-" * 63)
    print(f"{'Original Value':<30} | {'New Value':<30}")
    print("-" * 63)
    for old, new in zip(old_values, new_values):
        print(f"{str(old)[:30]:<30} | {str(new)[:30]:<30}")
    print("-" * 63)

def main():
    tinfoil_llm = TinfoilLLM()
    text = get_pdf_text(PDF_PATH)
    sensitive_data = get_sensitive_data(text, tinfoil_llm)
    if sensitive_data is None:
        print("Error: No sensitive data found")
        return
    old_values = post_process_sensitive_data(sensitive_data)
    new_values = assign_new_values(old_values, tinfoil_llm)
    print_mapping_table(old_values, new_values)
    create_pdfs(PDF_PATH, old_values, new_values)

if __name__ == "__main__":
    main()