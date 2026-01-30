## 2026-01-30 - Streamlit Caching and Dictionary Lookups
**Learning:** In Streamlit applications, frequent UI interactions trigger script reruns. Performing file I/O or O(N) list searches on every rerun significantly impacts responsiveness.
- Using `@st.cache_data` for disk-bound operations (like loading JSON/CSV results) eliminates redundant I/O.
- Transforming data structures from lists to dictionaries (hash maps) during the loading phase allows for O(1) lookups in subject-level analysis, further reducing computation time during UI interactions.
- Moving imports to the top level of the file avoids repeated dictionary lookups in `sys.modules` during script reruns.

**Action:** Always encapsulate expensive I/O and data processing in cached functions when developing for Streamlit. Prefer hash map lookups over sequential scans for frequently accessed data elements.
