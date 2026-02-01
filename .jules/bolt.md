
## 2025-05-14 - [O(1) lookups and Streamlit caching]
**Learning:** In applications with large per-subject datasets, O(N) list searches for individual subject reports cause linear performance degradation. Additionally, redundant disk I/O on every Streamlit interaction significantly slows down the UI.
**Action:** Use dictionaries for fast O(1) lookups by subject ID and leverage `@st.cache_data` to prevent redundant file reading in the main UI script.
