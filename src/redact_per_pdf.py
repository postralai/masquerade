import os
import fitz

from src.get_pdf_text import get_pdf_text
from src.get_sensitive_data import get_sensitive_data, post_process_sensitive_data


def mask_sensitive_data(sensitive_data):
    masked_sensitive_data = {}
    for subject, value_list in sensitive_data.items():
        masked_value_list = []
        for value in value_list:
            if isinstance(value, str):
                if '@' in value:  # Email address
                    username, domain = value.split('@')
                    masked_username = username[:2] + '*' * (len(username) - 2)
                    domain_parts = domain.split('.')
                    masked_domain = domain_parts[0][:2] + '*' * (len(domain_parts[0]) - 2)
                    masked_value = f"{masked_username}@{masked_domain}.{domain_parts[1]}"
                elif any(c.isdigit() for c in value):  # Phone number or ID
                    # Keep first 2 and last 2 digits, mask the rest
                    masked_value = value[:2] + '*' * (len(value) - 4) + value[-2:]
                else:  # Name or other text
                    # Keep first 2 characters, mask the rest
                    masked_value = value[:2] + '*' * (len(value) - 2)
                masked_value_list.append(masked_value)
            else:
                masked_value_list.append(value)
        masked_sensitive_data[subject] = masked_value_list
    return masked_sensitive_data

def redact_pdf(pdf_path):
    text = get_pdf_text(pdf_path)
    sensitive_data = get_sensitive_data(text)
    if sensitive_data is None:
        print("Error: No sensitive data found")
        return
    sensitive_values = post_process_sensitive_data(sensitive_data)
    file_basename = os.path.splitext(os.path.basename(pdf_path))[0]
    redacted_path = f"{file_basename}_redacted.pdf"
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    redaction_summary = {
        "total_pages": len(doc),
        "redacted_pages": [],
        "total_redactions": 0,
        "output_file": redacted_path
    }

    # Iterate through each page
    for page in doc:
        page_redacted_sections = {
            "page": page.number,
            "number_of_redactions": 0,
        }
        for sensitive_value in sensitive_values:
            # Get the text instances on the page
            text_instances = page.search_for(sensitive_value)
            
            # Redact each instance
            for inst in text_instances:
                page.add_redact_annot(inst)
            
            # Apply the redactions
            page.apply_redactions()

            if len(text_instances) > 0:
                page_redacted_sections["number_of_redactions"] += len(text_instances)
        redaction_summary["redacted_pages"].append(page_redacted_sections)
        redaction_summary["total_redactions"] += page_redacted_sections["number_of_redactions"]

    # Save the redacted PDF
    doc.save(redacted_path)
    doc.close()

    # Mask sensitive data
    masked_sensitive_data = mask_sensitive_data(sensitive_data)
    redaction_summary["masked_sensitive_data"] = masked_sensitive_data

    return redaction_summary

if __name__ == "__main__":
    redacted_path = redact_pdf("insurance_offer.pdf")
