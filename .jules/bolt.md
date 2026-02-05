## 2025-02-05 - Optimize result loading and subject lookups

**Learning:** Converting prediction lists to dictionaries for O(1) lookups provides a measurable ~8x speedup (0.0037s -> 0.00046s per check) for large datasets (N=20,000). Also, Streamlit's `@st.cache_data` is essential for avoiding redundant disk I/O on every UI interaction, especially when handling large CSVs and JSONs. Cache clearing (`st.cache_data.clear()`) is necessary when the underlying data is updated.

**Action:** Always prefer dictionary lookups over linear searches in results handling. Always wrap I/O operations in cached functions in Streamlit apps.
