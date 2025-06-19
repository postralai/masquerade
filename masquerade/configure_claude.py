import os
import json
import subprocess
import platform
import time

python_path = subprocess.check_output(['which', 'python'], text=True).strip()
mcp_script_path = subprocess.check_output(['python', '-c', 'import masquerade as m; print(f"{m.__path__[0]}/mcp_pdf_redaction.py")'], text=True).strip()
tinfoil_api_key = input("Enter your Tinfoil API key: ")

claude_config = {
    "mcpServers": {
        "pdf-redaction": {
            "command": python_path,
            "args": [mcp_script_path],
            "env": {
                "TINFOIL_API_KEY": tinfoil_api_key
            }
        }
    }
}

# Determine the correct config file path based on OS
system = platform.system()
if system == "Darwin":  # macOS
    config_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
elif system == "Windows":
    username = os.getenv('USERNAME') or os.getenv('USER')
    config_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Claude\\claude_desktop_config.json"
else:  # Linux
    config_path = os.path.expanduser("~/.config/Claude/claude_desktop_config.json")

access_to_config = input("Can I add the JSON to the Claude config file? (y/n) ")
if access_to_config not in ["y", "Y", "yes", "Yes", "YES"]:
    print("❌ Config not added to Claude config file.")
    print("❌ Please add it manually.")
    print("❌ Copy the following configuration into your Claude config JSON file:")
    time.sleep(3)
    print(json.dumps(claude_config, indent=2))
    exit()

# Check if config file exists
if os.path.exists(config_path):
    
    # Read existing config
    with open(config_path, 'r') as f:
        try:
            existing_config = json.load(f)
        except json.JSONDecodeError:
            existing_config = {}
    
    # Merge with new config
    if "mcpServers" not in existing_config:
        existing_config["mcpServers"] = {}
    
    existing_config["mcpServers"].update(claude_config["mcpServers"])
    
    # Write back to file
    with open(config_path, 'w') as f:
        json.dump(existing_config, f, indent=2)
    
    print("✅ Configuration successfully added to Claude config file!")
    print("✅ Restart Claude Desktop to apply the changes")
    
else:
    print("❌ Claude config file not found.")
    print("❌ Please create the config file manually or ensure Claude Desktop is installed.")
    print("❌ Copy the following configuration into your Claude config JSON file:")
    print(json.dumps(claude_config, indent=2))
