Streamlit UI for quick project runner

Quick start

1. (Optional) Create a virtual environment and install requirements:

   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

2. Run the UI locally:

   streamlit run app.py

What it does
- Provides checkboxes to select which projects to run and a single "Run Now" button. The page streams the stdout/stderr from the underlying `wrapper/quick_run.py` process and shows quick links/downloads to recent outputs.
- Designed for fast local inspection and demoing; it intentionally delegates execution to the conservative `quick_run.py` script to avoid triggering long training runs.

Notes
- For full functionality some tools are required on your PATH: `Rscript` (for ADNI R scripts) and `jupyter nbconvert` (for executing notebooks). If those are not installed, the UI will still run but certain steps will be skipped.
