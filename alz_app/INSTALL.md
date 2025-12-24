# Installation & Run Instructions

## Python environment

Create a new environment (recommended):

- with venv:
  python -m venv .venv
  .\.venv\Scripts\activate
  pip install --upgrade pip

- or with conda:
  conda create -n alzapp python=3.10
  conda activate alzapp

## Install Python deps

pip install streamlit

(Note: the wrappers only use Python standard library + streamlit.)

## Run the app

streamlit run app/main_ui.py

or

python run_app.py

## What to prepare manually

- Clone external repos into `alz_app/external/`:
  - TransMF_AD
  - LEAD
  - ADNI
  - TADPOLE
  - AD-Biomarkers-Project

- Place data into `alz_app/data/` following the structure described in the main spec:
  - `MRI_PET_ADNI/` with `MRI/`, `PET/`, `ADNI.csv`
  - `EEG_LEAD/` with `Feature/` and `Label/`
  - `ADNI_full/` with `ADNI_data/`, `CNN/`, `TADPOLE_raw/`
  - `Proteomics/` with `proteomics_raw.csv`

- Install R and any R packages needed for `ADNI` project if you plan to run R scripts.

- For each repo, follow its README to install project-specific dependencies if you will run them.
