## 2025-05-15 - [Streamlit Caching and Dictionary Lookups]
**Learning:** In Streamlit apps, the script reruns on every user interaction. Expensive operations like file I/O and large-scale iterations (e.g., building a subject list from O(N) lists) create significant latency. Converting to O(1) dictionary lookups and using `@st.cache_data` for both I/O and processing dramatically improves responsiveness.
**Action:** Always prefer dictionary lookups for ID-based data and use `@st.cache_data` for any logic that doesn't need to run on every rerun in Streamlit.
