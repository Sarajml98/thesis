Quick Run — minimal CLI wrapper

This tool provides a very small, fast CLI (`quick_run.py`) to run conservative/default actions for the five projects in the repository.

Purpose
- Provide quick validation that each project is present and can be invoked with a small, low-cost command.
- Collect basic outputs (logs, small produced files) into a timestamped folder under `wrapper_outputs/`.

How to use

From the `wrapper/` folder or root of repository, run:

    python wrapper/quick_run.py            # runs all projects using default quick commands (asks for confirmation)

To run only some projects non-interactively:

    python wrapper/quick_run.py --projects ADNI,LEAD --no-confirm

Change output location:

    python wrapper/quick_run.py --output-dir ./my_quick_outputs --no-confirm

Notes
- The script tries to use `Rscript` for R-based projects when available, and `jupyter nbconvert` for notebooks. If these tools are not installed or the expected data files are missing, the script will skip heavy operations and only write explanatory log lines.
- This is intentionally conservative — it avoids long training runs and aims to be quick to run and inspect.

If you'd like, I can now run `quick_run.py` here to show a live demonstration (it will only attempt quick operations and copy existing small outputs).