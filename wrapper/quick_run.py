"""quick_run.py

Minimal CLI to run quick/default commands for the five projects in this workspace.
- Defaults to running all projects non-interactively using lightweight commands
- Saves logs and copies known output folders into wrapper_outputs/<project>/<timestamp>/

Usage examples:
    python quick_run.py                       # run all projects with defaults
    python quick_run.py --projects ADNI,LEAD  # run selected projects
    python quick_run.py --output-dir ./out    # change output base

This tool intentionally keeps behavior conservative ("quick" runs) to avoid long training.
"""

import argparse
import os
import sys
import subprocess
import shutil
import time
from datetime import datetime
from pathlib import Path

PROJECTS = [
    "AD-Biomarkers-Project",
    "ADNI",
    "LEAD",
    "TADPOLE",
    "TransMF_AD",
]

ROOT = Path(__file__).resolve().parents[1]


def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def run_command(cmd, cwd, log_file):
    """Run a command and stream stdout/stderr to log_file."""
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Command: {' '.join(cmd)}\nWorking dir: {cwd}\n\n")
        f.flush()
        proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            f.write(line)
            f.flush()
            print(line, end="")
        proc.wait()
        return proc.returncode


def copy_if_exists(src, dst):
    """Copy file or folder if it exists."""
    src_p = Path(src)
    if not src_p.exists():
        return False
    dst_p = Path(dst)
    try:
        if src_p.is_dir():
            shutil.copytree(src_p, dst_p)
        else:
            dst_p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_p, dst_p)
        return True
    except Exception as e:
        print(f"Failed to copy {src} -> {dst}: {e}")
        return False


def handle_ad_biomarkers(project_path, out_dir, python_exec):
    logs = out_dir / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    log = logs / "ad_biomarkers.log"
    nb = project_path / "ModelsPipeline.ipynb"
    if nb.exists():
        print("Running ModelsPipeline.ipynb with nbconvert (quick)")
        out_html = out_dir / "ModelsPipeline.html"
        # check nbconvert availability
        try:
            rc_check = subprocess.run([python_exec, "-m", "nbconvert", "--version"], cwd=project_path, capture_output=True, text=True).returncode
        except Exception:
            rc_check = 1
        if rc_check != 0:
            print("nbconvert not available; skipping notebook execution. Install with 'pip install jupyter nbconvert'.")
            with open(log, "a") as f:
                f.write("nbconvert not available; skipped executing notebook. Install with 'pip install jupyter nbconvert'.\n")
        else:
            cmd = [python_exec, "-m", "nbconvert", "--execute", "--to", "html", str(nb), "--output", str(out_html)]
            rc = run_command(cmd, cwd=project_path, log_file=log)
            print(f"Return code: {rc}")
    else:
        print("No ModelsPipeline.ipynb found; skipping AD-Biomarkers quick run.")
        with open(log, "a") as f:
            f.write("No ModelsPipeline.ipynb found; nothing executed.\n")
    # copy figures/csvs if present
    for candidate in [project_path / "figures", project_path / "*.csv"]:
        try:
            # copy entire figures folder
            if (project_path / "figures").exists():
                copy_if_exists(project_path / "figures", out_dir / "figures")
        except Exception:
            pass


def handle_adni(project_path, out_dir):
    logs = out_dir / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    log = logs / "adni.log"
    # Run key R scripts if Rscript exists
    rscript = shutil.which("Rscript")
    if rscript:
        scripts = ["R/amyloid_pos.R", "R/stage1.R"]
        for scr in scripts:
            scr_path = project_path / scr
            if scr_path.exists():
                print(f"Running {scr} with Rscript")
                rc = run_command([rscript, str(scr_path)], cwd=project_path, log_file=log)
                print(f"Return code: {rc}")
            else:
                print(f"{scr} not found; skipping")
                with open(log, "a") as f:
                    f.write(f"{scr} not found; skipped.\n")
    else:
        print("Rscript not available on PATH; skipping ADNI R scripts. Install R to enable.")
        with open(log, "a") as f:
            f.write("Rscript not available on PATH; skipped running R scripts.\n")
    # copy processed_data and figures if present
    for candidate in [project_path / "processed_data", project_path / "figures", project_path / "CNN/trained_cn_ad_mri"]:
        if candidate.exists():
            copy_if_exists(candidate, out_dir / candidate.name)


def handle_lead(project_path, out_dir, python_exec):
    logs = out_dir / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    log = logs / "lead.log"
    run_py = project_path / "run.py"
    dataset_dir = project_path / "dataset"
    if run_py.exists():
        # run in test mode (is_training 0) to avoid long training
        cmd = [python_exec, str(run_py), "--method", "LEAD", "--task_name", "supervised", "--model", "LEAD", "--model_id", "quick-test", "--is_training", "0", "--root_path", str(dataset_dir)]
        print("Running LEAD in quick test mode (is_training=0)")
        rc = run_command(cmd, cwd=project_path, log_file=log)
        print(f"Return code: {rc}")
    else:
        print("LEAD run.py not found; skipping")
        with open(log, "a") as f:
            f.write("run.py not found; skipped.\n")
    # copy checkpoints and results if exist
    for c in [project_path / "checkpoints", project_path / "results", project_path / "figs"]:
        if c.exists():
            copy_if_exists(c, out_dir / c.name)


def handle_tadpole(project_path, out_dir, python_exec=None):
    logs = out_dir / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    log = logs / "tadpole.log"
    script = project_path / "TADPOLE_D1_D2.py"
    if script.exists():
        print("Running TADPOLE_D1_D2.py (quick)")
        python_exec_resolved = python_exec or sys.executable
        rc = run_command([python_exec_resolved, str(script), "--spreadsheetFolder", str(project_path)], cwd=project_path, log_file=log)
        print(f"Return code: {rc}")
    else:
        print("TADPOLE script not found; skipping")
        with open(log, "a") as f:
            f.write("TADPOLE script not found; skipped.\n")
    # copy evaluation outputs if present
    for c in [project_path / "evaluation"]:
        if c.exists():
            copy_if_exists(c, out_dir / c.name)


def handle_transmf(project_path, out_dir, python_exec):
    logs = out_dir / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    log = logs / "transmf.log"
    script = project_path / "kfold_train_adversarial.py"
    data_dir = project_path / "MRI"
    if script.exists():
        if data_dir.exists():
            print("Running TransMF quick k-fold trainer (small batch) using available MRI data")
            cmd = [python_exec, str(script), "--randint", "False", "--aug", "False", "--batch_size", "4", "--name", "quick_test", "--task", "ADCN", "--model", "CNN", "--dataroot", str(project_path)]
            rc = run_command(cmd, cwd=project_path, log_file=log)
            print(f"Return code: {rc}")
        else:
            print("TransMF data dir not found; skipping heavy training. If you want to run it, add MRI/PET data under the repo as described in README.")
            with open(log, "a") as f:
                f.write("No MRI data dir found; skipped heavy training.\n")
    else:
        print("TransMF trainer script not found; skipping")
        with open(log, "a") as f:
            f.write("kfold_train_adversarial.py not found; skipped.\n")
    # copy checkpoints if present
    for c in [project_path / "checkpoints"]:
        if c.exists():
            copy_if_exists(c, out_dir / c.name)


HANDLERS = {
    "AD-Biomarkers-Project": handle_ad_biomarkers,
    "ADNI": handle_adni,
    "LEAD": handle_lead,
    "TADPOLE": handle_tadpole,
    "TransMF_AD": handle_transmf,
}


def main():
    parser = argparse.ArgumentParser(description="Quick runner for the five projects (minimal, safe defaults)")
    parser.add_argument("--projects", type=str, default="all",
                        help="Comma-separated list of projects to run (or 'all'). Available: " + ",".join(PROJECTS))
    parser.add_argument("--output-dir", type=str, default=str(ROOT / "wrapper_outputs"), help="Base output directory")
    parser.add_argument("--python-exec", type=str, default=sys.executable, help="Python executable to use")
    parser.add_argument("--no-confirm", action="store_true", help="Do not ask confirmations; non-interactive")
    args = parser.parse_args()

    selected = args.projects.split(",") if args.projects != "all" else PROJECTS
    selected = [s.strip() for s in selected if s.strip()]

    # Validate projects
    valid = [p for p in selected if p in HANDLERS]
    invalid = set(selected) - set(valid)
    if invalid:
        print(f"Invalid projects ignored: {', '.join(invalid)}")

    # If no-confirm false and user didn't pass --no-confirm, confirm
    if not args.no_confirm and 'CI' not in os.environ:
        resp = input(f"Will run projects: {', '.join(valid)}. Proceed? [Y/n]: ")
        if resp.strip().lower().startswith('n'):
            print("Cancelled by user.")
            return

    base_out = Path(args.output_dir)
    base_out.mkdir(parents=True, exist_ok=True)

    summary = {}
    for proj in valid:
        print("\n", "=" * 30)
        print(f"Starting quick run for project: {proj}")
        proj_path = ROOT / proj
        out_dir = base_out / proj / timestamp()
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            handler = HANDLERS[proj]
            if proj == "AD-Biomarkers-Project":
                handler(proj_path, out_dir, args.python_exec)
            elif proj == "LEAD" or proj == "TransMF_AD":
                handler(proj_path, out_dir, args.python_exec)
            else:
                handler(proj_path, out_dir)
            summary[proj] = {"status": "done", "output": str(out_dir)}
        except Exception as e:
            print(f"Error while running {proj}: {e}")
            summary[proj] = {"status": "error", "error": str(e)}

    print("\nSummary:\n")
    for proj, info in summary.items():
        print(f"- {proj}: {info}")

    print(f"\nAll logs and copied outputs are under {base_out}")


if __name__ == '__main__':
    main()
