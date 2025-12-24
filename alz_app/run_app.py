"""Helper to run the Streamlit app with a simple python call (optional).

You can run the app with:
    streamlit run app/main_ui.py
or, if you prefer, with this small helper:
    python run_app.py
which will execute the correct streamlit CLI invocation.
"""
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main_ui.py"])
