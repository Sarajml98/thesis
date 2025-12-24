import streamlit as st
import subprocess
import sys
import os
import glob
import time
from pathlib import Path

# Config
REPO_ROOT = Path(__file__).resolve().parents[2]
QUICK_RUN = REPO_ROOT / "wrapper" / "quick_run.py"
DEFAULT_OUTPUT_DIR = str(REPO_ROOT / "wrapper_outputs")
PROJECTS = [
    "AD-Biomarkers-Project",
    "ADNI",
    "LEAD",
    "TADPOLE",
    "TransMF_AD",
]

st.set_page_config(page_title="AD Projects Runner", layout="wide")

# Simple CSS for a nicer look
st.markdown("""
<style>
section[data-testid="stSidebar"] {background-color: #f8f9fb}
h1 {color: #0b5cff}
.card {background: #ffffff; padding: 16px; border-radius: 8px; box-shadow: 0 1px 3px rgba(16,24,40,0.06);}
.code-area {background: #0b1220; color: #e6f0ff; padding: 8px; border-radius: 6px; font-family: monospace}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Runner — Quick UI")
    python_exec = st.text_input("Python executable", value=sys.executable)
    output_dir = Path(st.text_input("Output directory", value=DEFAULT_OUTPUT_DIR))
    run_parallel = st.checkbox("Run projects in parallel (not recommended)", value=False)
    show_advanced = st.checkbox("Show advanced options", value=False)
    st.markdown("---")
    st.markdown("Made for quick, local runs. Uses the conservative defaults from `wrapper/quick_run.py`.")
    st.button("Open outputs folder", on_click=lambda: os.startfile(output_dir) if output_dir.exists() else None)

# Main layout
st.title("Alzheimer Projects — Quick Runner UI ✨")
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Projects")
    selected = {}
    for proj in PROJECTS:
        with st.expander(proj, expanded=False):
            enabled = st.checkbox(f"Enable {proj}", value=True, key=f"chk_{proj}")
            selected[proj] = enabled
            if show_advanced:
                st.text("Advanced options")
                if proj == "LEAD":
                    is_training = st.selectbox("LEAD mode", ["test (is_training=0)", "train (is_training=1)"], key="lead_mode")
                elif proj == "AD-Biomarkers-Project":
                    st.checkbox("Execute ModelsPipeline.ipynb", value=True, key="ab_execute_nb")
                else:
                    st.write("No advanced options available for this project in quick mode.")

    st.markdown("---")
    k_choice = st.selectbox("Run scope", ["Run Selected", "Run All"], index=0)

    # Run buttons
    run_button = st.button("✅ Run Now")
    st.button("Clear logs", on_click=lambda: st.session_state.clear() if 'logs' in st.session_state else None)

with col2:
    st.subheader("Live Output")
    log_box = st.empty()
    status_box = st.empty()
    output_gallery = st.empty()

# Helper functions

def latest_project_output(base_out: Path, proj: str):
    p = base_out / proj
    if not p.exists():
        return None
    # pick most recent timestamp-named folder
    folders = [f for f in p.iterdir() if f.is_dir()]
    if not folders:
        return None
    latest = max(folders, key=lambda x: x.stat().st_mtime)
    return latest


def run_quick_run_cmd(projects, python_exec, output_dir, on_line):
    cmd = [python_exec, str(QUICK_RUN), "--projects", ",".join(projects), "--output-dir", str(output_dir), "--no-confirm"]
    process = subprocess.Popen(cmd, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        on_line(line)
    process.wait()
    return process.returncode


def show_outputs_for_projects(base_out: Path, projects):
    md = ""
    for proj in projects:
        latest = latest_project_output(base_out, proj)
        if latest is None:
            md += f"### {proj}: No outputs found yet.\n"
            continue
        md += f"### {proj}: {latest.name}\n"
        files = list(latest.rglob("*"))
        if not files:
            md += "(No files found)\n"
            continue
        for f in files:
            if f.is_dir():
                continue
            rel = f.relative_to(latest)
            size_mb = f.stat().st_size / (1024 * 1024)
            if size_mb < 10:
                with open(f, "rb") as fh:
                    btn = st.download_button(label=f"Download {proj}/{rel}", data=fh.read(), file_name=str(rel))
            else:
                md += f"- {rel} — {size_mb:.1f} MB — path: `{str(f)}`\n"
    output_gallery.markdown(md)

# Run logic
if run_button:
    projects_to_run = [p for p, v in selected.items() if v] if k_choice == "Run Selected" else PROJECTS
    if not projects_to_run:
        st.warning("No projects selected to run.")
    else:
        st.info(f"Running: {', '.join(projects_to_run)}")
        st.session_state['logs'] = ""
        def write_line(line):
            st.session_state['logs'] += line
            log_box.code(st.session_state['logs'][-10000:])

        # Run sequentially (simple and safe)
        start = time.time()
        rc = run_quick_run_cmd(projects_to_run, python_exec, output_dir, write_line)
        elapsed = time.time() - start
        status_box.success(f"Run completed in {elapsed:.1f}s (rc={rc})")
        # show outputs
        show_outputs_for_projects(output_dir, projects_to_run)
        st.balloons()

# Footer
st.markdown("---")
st.caption("This is a lightweight UI that delegates execution to `wrapper/quick_run.py`. For full configuration, edit the script or use the command line.")
