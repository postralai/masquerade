from get_pdf_text import get_pdf_text
from get_sensitive_data import get_sensitive_data
from assign_new_values import assign_new_value_with_llm
from swap_text_pdf import create_pdfs
from remove_values import remove_unchanged_words

PDF_PATH = "ok_org.pdf"

def main():
    text = get_pdf_text(PDF_PATH)
    sensitive_data = get_sensitive_data(text)
    if sensitive_data is None:
        print("Error: No sensitive data found")
        return
    old_values = [item for value in sensitive_data.values() if value and value is not None for item in (value if isinstance(value, list) else [value])]
    # Split values that contain commas into separate elements
    expanded_values = []
    for value in old_values:
        if isinstance(value, str) and ',' in value:
            # Split by comma and strip whitespace from each part
            parts = [part.strip() for part in value.split(',')]
            expanded_values.extend(parts)
        else:
            expanded_values.append(value)
    old_values = expanded_values
    old_values = remove_unchanged_words(old_values)
    new_values = []
    for value in old_values:
        if value is not None:
            try:
                new_value = assign_new_value_with_llm(value)
                new_values.append(new_value)
            except Exception as e:
                print(f"Error processing value '{value}': {str(e)}")
                continue
    # Print a table of old and new values
    print("\nValue Mappings:")
    print("-" * 63)
    print(f"{'Original Value':<30} | {'New Value':<30}")
    print("-" * 63)
    for old, new in zip(old_values, new_values):
        print(f"{str(old)[:30]:<30} | {str(new)[:30]:<30}")
    print("-" * 63 + "\n")
    create_pdfs(PDF_PATH, old_values, new_values)

if __name__ == "__main__":
    main()