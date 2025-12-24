# AlzMultiModal Analyzer (Demo)

This demo contains a Streamlit UI and lightweight wrappers for five external
Alzheimer's research codebases. The wrappers simulate results if the external
repos are not present, so the UI is useful for demos and can be easily
connected to real pipelines once you clone the projects into `external/`.

Structure (important):

alz_app/
  app/
    main_ui.py        # Streamlit UI
    backend.py        # Orchestration
    *.py              # module wrappers and helpers
  external/          # clone the 5 repos here
  data/              # place your data here
  outputs/           # pipeline summaries will be written here

See the `INSTALL.md` for steps to prepare your environment.
