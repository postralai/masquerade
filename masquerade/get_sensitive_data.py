import requests
import json
from masquerade.get_pdf_text import get_pdf_text
from masquerade.remove_values import remove_unchanged_words

def get_sensitive_data(text, tinfoil_llm):
    def get_sensitive_data_from_page(page_text, page_number=None):
        for i in range(5):
            prompt = f"""Fill the JSON below based on the text provided.
{{
    company_names: [],
    company_addresses: [],
    company_ids: [],
    all_emails: [],
    all_phone_numbers: [],
    contract_numbers: [],
    people_names: [],
    birth_dates: [],
    people_ids: [],
    customer_number: [],
}}
Do not include policy details, coverage terms, prices, or any other non-personal data.
Return the result as a single JSON dictionary with no nested structures.
Only return single valid JSON object, with no explanations.\n\n{text}"""
            if page_number is not None:
                print(f"Starting to extract sensitive data from page {page_number}...")
            else:
                print("Starting to extract sensitive data...")
            response = tinfoil_llm.get_tinfoil_response(prompt, model="deepseek")
            try:
                response = response.replace("```json", "").replace("```", "")
                sensitive_data = json.loads(response)
                print("Sensitive data extracted")
                return sensitive_data
            except json.JSONDecodeError:
                print(response)
        return {}

    def combine_values(old_value, new_value):
        if old_value is None:
            return new_value
        if new_value is None:
            return old_value
        
        # Convert both to lists if they aren't already
        old_list = old_value if isinstance(old_value, list) else [old_value]
        new_list = new_value if isinstance(new_value, list) else [new_value]
        
        # Combine lists and remove duplicates while preserving order
        combined = []
        seen = set()
        for item in old_list + new_list:
            if item not in seen:
                seen.add(item)
                combined.append(item)
        return combined

    if isinstance(text, list):
        sensitive_data = {}
        for i, page_text in enumerate(text, start=1):
            sensitive_data_page = get_sensitive_data_from_page(page_text, i)
            # Combine values instead of updating
            for key, new_value in sensitive_data_page.items():
                if key in sensitive_data:
                    sensitive_data[key] = combine_values(sensitive_data[key], new_value)
                else:
                    sensitive_data[key] = new_value
            print(sensitive_data)
        return sensitive_data
    else:
        return get_sensitive_data_from_page(text)

def post_process_sensitive_data(sensitive_data):
    sensitive_values = [item for value in sensitive_data.values() if value and value is not None for item in (value if isinstance(value, list) else [value])]
    # Split values that contain commas into separate elements
    expanded_values = []
    for subject, value_list in sensitive_data.items():
        for value in value_list:
            if isinstance(value, str) and ',' in value:
                # Split by comma and strip whitespace from each part
                parts = [part.strip() for part in value.split(',')]
                expanded_values.extend(parts)
            else:
                expanded_values.append(value)
    sensitive_values = remove_unchanged_words(expanded_values)
    return sensitive_values


if __name__ == "__main__":
    text = get_pdf_text("ok_org.pdf")
    sensitive_data_json = get_sensitive_data(text)
    print(sensitive_data_json)
    dict = json.loads(sensitive_data_json)
    print()
    print()
    print()
    print()
    print()
    for key, value in dict.items():
        print(f"{key}: {value}")
