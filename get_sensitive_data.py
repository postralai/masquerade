from get_pdf_text import get_pdf_text
import requests
import json

def get_sensitive_data(text):
    def get_sensitive_data_from_page(page_text, page_number=None):
        for i in range(10):
            prompt = f"""You are an information extraction engine. From the following insurance document, extract only the personally identifiable information (PII) related to the customer and the insurer.
Extract the following fields if available:
    company_names
    company_addresses
    company_ids (company registration numbers)
    all_emails
    all_phone_numbers
    contract_numbers
    people_names (names of any individuals mentioned)
    birth_dates
    people_ids (personal identity numbers)
    customer_number
Do not include policy details, coverage terms, prices, or any other non-personal data.
Return the result as a single JSON dictionary with all fields, using [] for missing ones.
Do not add explanations or text outside the JSON output.\n\n{text}"""
            if page_number is not None:
                print(f"Starting to extract sensitive data from page {page_number}...")
            else:
                print("Starting to extract sensitive data...")
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                response = response.json()["response"]
                try:
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
