from get_pdf_text import get_pdf_text
import requests

def get_sensitive_data(text):
    prompt = f"""You are an information extraction engine. From the following insurance document, extract only the personally identifiable information (PII) related to the customer and the insurer.
Extract the following fields if available:
    company_names
    company_addresses
    company_ids (company registration numbers)
    emails
    phone_numbers
    contract_numbers
    people_names (names of any individuals mentioned)
    customer_number
Do not include policy details, coverage terms, prices, or any other non-personal data.
Return the result as a single JSON dictionary with all fields, using null for missing ones.
Do not add explanations or text outside the JSON output.\n\n{text}"""
    print("Starting to extract sensitive data...")
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    print("Sensitive data extracted")
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code} - {response.text}"

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
