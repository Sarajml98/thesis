"""Combine module outputs into a single, plain-language final summary."""
from typing import Dict


def build_final_summary(results: Dict[str, dict]) -> str:
    """Build a short human readable paragraph summarizing modality results.

    Args:
        results: dict with keys 'mri_pet','eeg','adni','tadpole','proteomics'
    Returns:
        single paragraph string
    """
    lines = []

    m = results.get("mri_pet")
    if m and m.get("status") == "success":
        lines.append(f"MRI+PET: {m.get('interpretation', 'No interpretation available')}")
    else:
        lines.append("MRI+PET: no valid result.")

    e = results.get("eeg")
    if e and e.get("status") == "success":
        lines.append(f"EEG: {e.get('interpretation', 'No interpretation available')}")
    else:
        lines.append("EEG: no valid result.")

    a = results.get("adni")
    if a and a.get("status") == "success":
        lines.append(f"ADNI: {a.get('interpretation', 'No interpretation available')}")
    else:
        lines.append("ADNI: no valid result.")

    t = results.get("tadpole")
    if t and t.get("status") == "success":
        lines.append(f"TADPOLE: {t.get('interpretation', 'No interpretation available')}")
    else:
        lines.append("TADPOLE: no valid result.")

    p = results.get("proteomics")
    if p and p.get("status") == "success":
        lines.append(f"Proteomics: {p.get('interpretation', 'No interpretation available')}")
    else:
        lines.append("Proteomics: no valid result.")

    # One-line synthesis
    synth = " ".join([l for l in lines])
    return synth
