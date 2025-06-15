from src.redact_per_pdf import redact_pdf
from pprint import pprint


if __name__ == "__main__":
    redaction_summary = redact_pdf("insurance_offer.pdf")
    print("\nRedaction Summary:")
    pprint(redaction_summary, indent=2, width=100)
    
