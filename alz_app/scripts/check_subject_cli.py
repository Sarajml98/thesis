"""CLI helper to load outputs and show per-subject report (debugging aid)."""
import argparse
import json
from pathlib import Path
from app import backend

parser = argparse.ArgumentParser(description="Check subject from outputs folder")
parser.add_argument("subject_id", help="Subject ID to check (e.g. SUBJ001)")
parser.add_argument("--outputs", default="outputs", help="Path to outputs folder")
args = parser.parse_args()

out = Path(args.outputs)
results = {}
# Try aggregate
agg = out / "aggregate_results.json"
if agg.exists():
    results = json.load(open(agg, "r", encoding="utf-8"))
else:
    for name in ["mri_pet", "eeg", "adni", "tadpole", "proteomics"]:
        p = out / f"{name}_summary.json"
        if p.exists():
            results[name] = json.load(open(p, "r", encoding="utf-8"))
            preds = out / f"{name}_predictions.csv"
            if preds.exists():
                import csv
                rows = []
                with open(preds, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        rows.append({"subject_id": row.get("subject_id"), "predicted_label": row.get("predicted_label"), "probability": float(row.get("probability", 0))})
                results[name]["predictions"] = rows

report = backend.predict_subject(args.subject_id, results)
print(json.dumps(report, indent=2, ensure_ascii=False))
