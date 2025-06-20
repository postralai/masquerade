#!/bin/bash
set -e
python3.12 -m venv pdfmcp
source pdfmcp/bin/activate
pip install git+https://github.com/postralai/masquerade@main
python -m masquerade.configure_claude