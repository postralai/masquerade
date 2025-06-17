# Replace PDF text

Hide sensitive information from PDFs locally

![Image](https://github.com/user-attachments/assets/96002c8b-5839-4499-814e-e603d95e7c82)

## Installation

Install [Claude desktop](https://claude.ai/download)

```bash
git clone git@github.com:postralai/replace-pdf-text.git
pip install -r requirements.txt
```

## Configuration

1. Get Python path: `which python`
1. Get [Tinfoil](https://tinfoil.sh) API key (create account and API key)
1. Add the JSON below to `claude_desktop_config.json`. Instructions to find the config are in the image.

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

