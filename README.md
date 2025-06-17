# Masquerade MCP: Redact. Replace. Retain Control.

🤐 **Problem:** Tools like Claude or GPT are incredibly powerful—but they require raw input. If you're dealing with contracts, medical records, or internal documents, that's risky.

🛡️ **Solution:** Masquerade acts as a privacy firewall for your files. Just drag and drop a PDF, and Masquerade will:

Automatically detect sensitive data (names, emails, dates, entities)

Redact or replace it with pseudonyms

Let you preview + edit before sending to an LLM

![Image](https://github.com/user-attachments/assets/96002c8b-5839-4499-814e-e603d95e7c82)

## Installation

1. Install [Claude desktop](https://claude.ai/download)
1. Clone the repo and install requirements

```bash
git clone git@github.com:postralai/replace-pdf-text.git
pip install -r requirements.txt
```

## Configuration

1. Get Python path: `which python`
1. Get [Tinfoil](https://tinfoil.sh) API key (create account and API key)
1. Add (1) Python path, (2) MCP file path, and (3) Tinfoil API key to the JSON below and add that to `claude_desktop_config.json`. Instructions to find the config are in the image below.

```json
{
  "mcpServers": {
    "pdf-redaction": {
        "command": "/path/to/python",
        "args": ["/path/to/mcp_pdf_redaction.py"],
        "env": {
          "TINFOIL_API_KEY": "your_api_key"
        }
    }
  }
}
```

![Image](https://github.com/user-attachments/assets/cfa56a1a-bec0-40e5-95d9-f4f36c43b95a)

