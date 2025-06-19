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
1. Create a virtual environment with Python ">=3.10, <=3.12"
1. Install this repo with the command below

```bash
pip install git+https://github.com/postralai/masquerade@main
```

## Configuration

### Easy configuration

```bash
python -m masquerade.configure_claude
```

If successfully configured, then restart.

<details>
<summary><strong>Manual configuration (click to expand)</strong></summary>

### Manual configuration

1. Get Python path: `which python`
1. Get MCP file path: `python -c "import masquerade as m; print(f'{m.__path__[0]}/mcp_pdf_redaction.py')"`
1. Get [Tinfoil](https://tinfoil.sh) API key (create account and API key)
1. Add (1) Python path, (2) MCP file path, and (3) Tinfoil API key to the JSON below and add that to `claude_desktop_config.json`. Instructions to find the config file are in the image below.
1. Restart Claude.

```json
{
  "mcpServers": {
    "pdf-redaction": {
        "command": "/path/to/python", // Run `which python`
        "args": ["/path/to/mcp_pdf_redaction.py"], // Run `python -c "import masquerade as m; print(f'{m.__path__[0]}/mcp_pdf_redaction.py')"`
        "env": {
          "TINFOIL_API_KEY": "your_api_key" // Create Tinfoil account and paste API key
        }
    }
  }
}
```

![Image](https://github.com/user-attachments/assets/cfa56a1a-bec0-40e5-95d9-f4f36c43b95a)

</details>


## Contributing

If you have a fix or improvement, feel free to submit a pull request. For significant changes, please open an issue first to discuss your proposed updates.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Need Help?

For questions and common issues, please see the [FAQ section](faq.md) or open an issue on GitHub.
