# Bolt's Journal - AlzMultiModal Analyzer

## 2026-02-04 - Dictionary-based Lookups and Import Relocation
**Learning:** List-based searching for subjects across multiple modules scales poorly ((M \times N)$). Using dictionaries for predictions provides (1)$ lookup per module. Also, relocating imports to the top level in Streamlit apps prevents redundant lookups on every rerun.
**Action:** Convert prediction lists to dictionaries and move imports to the top of the file.
