"""High-level orchestration: run all modules and collect results.

The `run_all_analyses` function accepts a `progress_hook(module, status, fraction, msg)`
callable used by the UI to get live updates while the work runs.
"""
from pathlib import Path
from . import mri_pet_module, eeg_module, adni_module, tadpole_module, proteomics_module

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = BASE_DIR / "outputs"


def run_all_analyses(data_root: str, simulate_if_missing: bool = True, progress_hook=None) -> dict:
    """Run all pipelines in sequence, reporting progress via progress_hook.

    Returns a dict with keys: 'mri_pet','eeg','adni','tadpole','proteomics' mapping to
    each module's summary dict.
    """
    results = {}
    modules = [
        ("mri_pet", mri_pet_module.run_mri_pet),
        ("eeg", eeg_module.run_eeg),
        ("adni", adni_module.run_adni_pipeline),
        ("tadpole", tadpole_module.run_tadpole),
        ("proteomics", proteomics_module.run_proteomics),
    ]

    total = len(modules)
    for i, (name, func) in enumerate(modules, start=1):
        frac = (i - 1) / total
        if progress_hook:
            progress_hook(name, "queued", frac, f"About to run {name}")
        # Call the module with the same progress hook so substeps propagate
        try:
            summary = func(data_root, simulate_if_missing=simulate_if_missing, progress_hook=progress_hook)
        except Exception as e:
            summary = {"status": "error", "interpretation": f"Module raised exception: {e}"}
        results[name] = summary
        if progress_hook:
            progress_hook(name, summary.get("status", "finished"), i / total, summary.get("interpretation", ""))

    # Optionally, write an aggregate JSON
    import json
    (OUTPUTS_DIR / "aggregate_results.json").parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUTS_DIR / "aggregate_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results


def predict_subject(subject_id: str, results: dict, threshold: float = 0.5) -> dict:
    """Predict a single subject by aggregating module predictions.

    Args:
        subject_id: id string (e.g. SUBJ001)
        results: dict returned by run_all_analyses
        threshold: probability threshold to classify as AD

    Returns a dict with per-module predictions, ensemble probability and label.
    """
    import json
    from pathlib import Path

    per_module = {}
    probs = []
    weights = []
    missing = []

    for name, summary in results.items():
        pred = None
        # try inline predictions first
        preds = summary.get("predictions")
        if preds:
            for p in preds:
                if p.get("subject_id") == subject_id:
                    pred = p
                    break
        # else try to read predictions CSV
        if pred is None and summary.get("predictions_path"):
            try:
                import csv
                with open(summary["predictions_path"], "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get("subject_id") == subject_id:
                            pred = {"subject_id": row.get("subject_id"), "predicted_label": row.get("predicted_label"), "probability": float(row.get("probability", 0))}
                            break
            except Exception:
                pred = None
        if pred is None:
            per_module[name] = {"status": "missing", "interpretation": summary.get("interpretation", "")}
            missing.append(name)
            continue
        prob = float(pred.get("probability", 0.0))
        label = pred.get("predicted_label")
        per_module[name] = {"status": "ok", "probability": prob, "label": label}
        # weight by available metric: prefer auc then accuracy then 1.0
        weight = 1.0
        if summary.get("auc"):
            weight = float(summary.get("auc"))
        elif summary.get("accuracy"):
            weight = float(summary.get("accuracy"))
        elif (summary.get("metrics") or {}).get("auc"):
            weight = float((summary.get("metrics") or {}).get("auc"))
        probs.append(prob * weight)
        weights.append(weight)

    ensemble = {"available_modules": len(weights), "missing_modules": missing}
    if weights:
        ensemble_prob = float(sum(probs) / sum(weights))
        ensemble_label = "AD" if ensemble_prob >= threshold else "CN"
    else:
        ensemble_prob = None
        ensemble_label = "unknown"

    ensemble.update({"probability": ensemble_prob, "label": ensemble_label})

    # Build a short final verdict text in Persian and an English disclaimer
    if ensemble_prob is None:
        final_text = "نتیجه نهایی: نامعلوم (هیچ پیش‌بینی ماژولی در دسترس نیست)."
        final_label = "unknown"
    else:
        if ensemble_label == "AD":
            final_text = f"نتیجه نهایی: بیمار **مبتلا به آلزایمر** تشخیص داده شد (احتمال = {ensemble_prob:.3f})."
        else:
            final_text = f"نتیجه نهایی: بیمار **مبتلا به آلزایمر نیست** (احتمال = {ensemble_prob:.3f})."
        final_label = ensemble_label
    disclaimer = "توجه: این یک پیش‌بینی مدل است و تشخیص بالینی محسوب نمی‌شود."

    # Save a subject-level report
    out_dir = Path(OUTPUTS_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"subject_{subject_id}_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "subject_id": subject_id,
            "per_module": per_module,
            "ensemble": ensemble,
            "final_label": final_label,
            "final_text": final_text,
            "disclaimer": disclaimer,
        }, f, indent=2)

    return {"subject_id": subject_id, "per_module": per_module, "ensemble": ensemble, "report_path": str(out_path), "final_label": final_label, "final_text": final_text}
