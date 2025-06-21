from mcp.server.fastmcp import FastMCP
import os
import subprocess
from masquerade import redact_pdf
from masquerade.tinfoil_llm import TinfoilLLM

# Create a FastMCP server instance
mcp = FastMCP(name="PDFRedactionServer")
tinfoil_llm = TinfoilLLM()

@mcp.tool("redact_pdf")
def process_pdf(params):
    pdf_path = None

    try:
        if isinstance(params, str):
            pdf_path = params
        elif isinstance(params, dict):
            # Try to get path from any reasonable key
            for key in ["pdf_path", "path", "file_path", "filename", "file"]:
                if key in params:
                    pdf_path = params[key]
                    break

            # If no named key found, try the first value
            if not pdf_path and params:
                pdf_path = next(iter(params.values()))
    except Exception as e:
        return {"success": False, "error": f"Parameter parsing error: {str(e)}"}

    if not pdf_path:
        return {"success": False, "error": "No PDF path provided"}

    # Check if file exists and is a PDF
    if not os.path.exists(pdf_path):
        return {"success": False, "error": f"File not found: {pdf_path}"}
    
    if not pdf_path.lower().endswith(".pdf"):
        return {"success": False, "error": "File is not a PDF"}

    try:
        redaction_summary, highlighted_path = redact_pdf(pdf_path, tinfoil_llm)

        try:
            subprocess.run(["open", redaction_summary["redacted_pdf_path"]], check=True)
            subprocess.run(["open", highlighted_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not open PDF file: {e}")
        except FileNotFoundError:
            try:
                subprocess.run(["xdg-open", redaction_summary["redacted_pdf_path"]], check=True)
                subprocess.run(["xdg-open", highlighted_path], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"Warning: Could not open PDF file automatically")

        return {
            "success": True,
            "redaction_summary": redaction_summary
        }
    except Exception as e:
        return {"success": False, "error": f"Error processing PDF file: {str(e)}"}

# Define a resource: expose PDF redaction summary endpoint
@mcp.resource("pdf://redact")
def redact_pdf_endpoint():
    return {
        "meta": None,
        "contents": [{
            "uri": "pdf://redact",
            "mime_type": "application/json",
            "text": "PDF redaction summary endpoint"
        }]
    }

if __name__ == "__main__":
    mcp.run()
