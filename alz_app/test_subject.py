from app import backend
import json

# Run all analyses in simulate mode (uses demo predictions)
results = backend.run_all_analyses('.\\data', simulate_if_missing=True)
# Check a sample subject
subject_id = 'SUBJ001'
report = backend.predict_subject(subject_id, results)
print(json.dumps(report, indent=2, ensure_ascii=False))
