# Masquerade MCP: Redact. Replace. Retain Control.

🤐 **Problem:** Tools like Claude or GPT are incredibly powerful—but they require raw input. If you're dealing with contracts, medical records, or internal documents, that's risky.

🛡️ **Solution:** Masquerade acts as a privacy firewall for your files. Just drag and drop a PDF, and Masquerade will:

Automatically detect sensitive data (names, emails, dates, entities)

Redact or replace it with pseudonyms

Let you preview + edit before sending to an LLM

## Architechture

![Image](https://github.com/user-attachments/assets/96002c8b-5839-4499-814e-e603d95e7c82)

1. User prompts Claude "Redact this PDF: /path/to/filename.pdf"
1. MCP receives the path, reads the PDF, converts it to text
1. Tinfoil receives the PDF text which is a secure AI platform that has no access to any data that is sent there
1. Tinfoil runs Llama 3.3 70b model to find the sensitive data
1. MCP removes the sensitive data from the PDF and writes a new redacted PDF to a temp folder
1. The MCP returns redaction summary to Claude. That includes masked values of the sensitive data (2 first charactes), page specific number of redactions, and the path to the redacted PDF.
1. Claude will either print the redacted PDF path or the user has to ask for it
1. The user can now upload the redacted PDF to Claude and start quering it if he/she feels comfortable with the applied redactions.

## Installation

1. Install [Claude desktop](https://claude.ai/download)
1. Clone the repo and install requirements

```bash
git clone git@github.com:postralai/masquerade.git
pip install -r requirements.txt
```

## Configuration

1. Get Python path: `which python`
1. Get [Tinfoil](https://tinfoil.sh) API key (create account and API key)
1. Add (1) Python path, (2) MCP file path, and (3) Tinfoil API key to the JSON below and add that to `claude_desktop_config.json`. Instructions to find the config file are in the image below.

```json
{
  "mcpServers": {
    "pdf-redaction": {
        "command": "/path/to/python", // Run `which python`
        "args": ["/path/to/mcp_pdf_redaction.py"], // cd into the repo, run `pwd`
        "env": {
          "TINFOIL_API_KEY": "your_api_key" // Create Tinfoil account and paste API key
        }
    }
  }
}
```

![Image](https://github.com/user-attachments/assets/cfa56a1a-bec0-40e5-95d9-f4f36c43b95a)

## Contributing

If you have a fix or improvement, feel free to submit a pull request. For significant changes, please open an issue first to discuss your proposed updates.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Need Help?

For questions and common issues, please see the [FAQ section](faq.md) or open an issue on GitHub.
