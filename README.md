# Masquerade MCP: Redact. Replace. Retain Control.

[![Demo video](https://github.com/user-attachments/assets/27e1580b-6fde-474c-8e88-44e77c3fb6a0)](https://github.com/user-attachments/assets/80b1d8ac-a012-41ce-8e92-64d567f2427f)

🤐 **Problem:** Tools like Claude or GPT are incredibly powerful, but they require raw input. If you're dealing with contracts, medical records, or internal documents, that's risky.

🛡️ **Solution:** Masquerade acts as a privacy firewall for your files. Just paste in the **file path** to a PDF, and Masquerade will:

  - Automatically detect sensitive data (names, emails, dates, entities)
  - Redact the sensitive data
  - Let you preview before sending to an LLM

## Architecture

![Image](https://github.com/user-attachments/assets/96002c8b-5839-4499-814e-e603d95e7c82)

1. **User Input**: The user asks Claude to redact a PDF by providing its file path.
1. **PDF Processing**: MCP reads the PDF and converts it to text.
1. **Sensitive Data Detection**: The text is sent to Tinfoil (an isolated AI platform using Llama 3.3 70B) to identify sensitive data.
1. **Redaction**: MCP removes the sensitive data and creates a redacted PDF.
1. **Summary Return**: MCP sends Claude a summary with:
    - Masked versions of the sensitive data
    - Redaction counts per page
    - The path to the redacted file
1. **Quering PDF with Claude**: The user can upload the redacted PDF to Claude if satisfied with the redactions.

## Installation

[![Setup video](https://github.com/user-attachments/assets/1402cd40-34df-4776-a8e4-f07d6f20c90b)](https://github.com/user-attachments/assets/76dedb64-1ef5-4ab4-afe1-11f399b3653b)

1. Install [Claude desktop](https://claude.ai/download)
1. Get [Tinfoil](https://tinfoil.sh) API key (create account and API key)
1. Configure environment

<details open>
<summary><strong>Option 1: Automated</strong></summary>

```bash
curl -O https://raw.githubusercontent.com/postralai/masquerade/main/setup.sh && bash setup.sh
```

4. Restart Claude desktop app (if successfully configured)

</details>

<details>
<summary><strong>Option 2: Manual (click to expand)</strong></summary>

4. Create a virtual environment with **Python ">=3.10, <=3.12"**

```bash
python3.12 -m venv pdfmcp
source pdfmcp/bin/activate
python --version
```

5. Install this repo with the command below

```bash
pip install git+https://github.com/postralai/masquerade@main
```

6. Automate the Claude config setup (and skip the next steps)

```bash
python -m masquerade.configure_claude
```

7. Get Python path: `which python`
1. Get MCP file path: `python -c "import masquerade as m; print(f'{m.__path__[0]}/mcp_pdf_redaction.py')"`
1. Add (1) Python path, (2) MCP file path, and (3) Tinfoil API key to the JSON below and add that to `claude_desktop_config.json`. Instructions to find the config file are in the image below.
1. Restart Claude

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

## How to use?

1. Prompt Claude: "Redact sensitive information from this PDF: /path/to/filename.pdf"
1. MCP opens the redacted and highlighted PDF files
1. Manually upload the redacted PDF to Claude for quering

**Note:** Don't upload the original PDF to Claude, only the file path.

## Contributing

If you have a fix or improvement, feel free to submit a pull request. For significant changes, please open an issue first to discuss your proposed updates.

See the [Developer section](docs/developers.md) for the installation of this repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Need Help?

For questions and common issues, please see the [FAQ section](docs/faq.md) or open an issue on GitHub.
