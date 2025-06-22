import os
import fitz
import tempfile

from masquerade.get_pdf_text import get_pdf_text
from masquerade.get_sensitive_data import get_sensitive_data, post_process_sensitive_data


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

def apply_redactions(pdf_path, sensitive_values):
    # Open the PDF
    doc_redacted = fitz.open(pdf_path)
    doc_highlighted = fitz.open(pdf_path)
    
    redaction_summary = {
        "total_pages": len(doc_redacted),
        "redacted_pages": [],
        "total_redactions": 0
    }

    # Iterate through each page
    for page_redacted, page_highlighted in zip(doc_redacted, doc_highlighted):
        page_redacted_sections = {
            "page": page_redacted.number,
            "number_of_redactions": 0,
        }
        for sensitive_value in sensitive_values:
            text_instances = page_redacted.search_for(sensitive_value)
            for inst in text_instances:
                highlight = page_highlighted.add_highlight_annot(inst)
                highlight.update()
                page_redacted.add_redact_annot(inst)
            page_redacted.apply_redactions()
            if len(text_instances) > 0:
                page_redacted_sections["number_of_redactions"] += len(text_instances)
        redaction_summary["redacted_pages"].append(page_redacted_sections)
        redaction_summary["total_redactions"] += page_redacted_sections["number_of_redactions"]

    # Save the redacted PDF
    try:
        # Create to same directory as the original PDF
        redacted_path = pdf_path.replace(".pdf", "_redacted.pdf")
        highlighted_path = pdf_path.replace(".pdf", "_highlighted.pdf")
        doc_redacted.save(redacted_path)
        doc_highlighted.save(highlighted_path)
    except:
        # Create to temporary directory
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            redacted_path = temp_file.name
        highlighted_path = redacted_path.replace(".pdf", "_highlighted.pdf")
        doc_redacted.save(redacted_path, garbage=4, deflate=True, clean=True)
        doc_highlighted.save(highlighted_path, garbage=4, deflate=True, clean=True)
    doc_redacted.close()
    doc_highlighted.close()
    redaction_summary["redacted_pdf_path"] = redacted_path

    return redaction_summary, highlighted_path

def redact_pdf(pdf_path, tinfoil_llm):
    text = get_pdf_text(pdf_path)
    sensitive_data = get_sensitive_data(text, tinfoil_llm)
    if sensitive_data is None:
        print("Error: No sensitive data found")
        return
    sensitive_values = post_process_sensitive_data(sensitive_data)

    redaction_summary, highlighted_path = apply_redactions(pdf_path, sensitive_values)

    # Mask sensitive data
    masked_sensitive_data = mask_sensitive_data(sensitive_data)
    redaction_summary["masked_sensitive_data"] = masked_sensitive_data

    return redaction_summary, highlighted_path

if __name__ == "__main__":
    from tinfoil_llm import TinfoilLLM
    tinfoil_llm = TinfoilLLM()
    redacted_path = redact_pdf("insurance_offer.pdf", tinfoil_llm)
