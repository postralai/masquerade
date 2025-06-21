from src.masquerade.redact_per_pdf import redact_pdf
from src.masquerade.tinfoil_llm import TinfoilLLM
from pprint import pprint


if __name__ == "__main__":
    tinfoil_llm = TinfoilLLM()
    redaction_summary = redact_pdf("insurance_offer.pdf", tinfoil_llm)
    print("\nRedaction Summary:")
    pprint(redaction_summary, indent=2, width=100)
    
