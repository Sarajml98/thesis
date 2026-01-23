# Bolt's Journal ⚡

## 2024-07-25 - Streamlit I/O Anti-Pattern
**Learning:** Reading files directly within a Streamlit script's main body is a significant performance anti-pattern. The script re-executes on every user interaction (e.g., button click, dropdown selection), leading to repeated and unnecessary file I/O operations that slow down the UI response time.
**Action:** Always encapsulate expensive data loading operations, especially file I/O, into dedicated functions. Apply the `@st.cache_data` decorator to these functions. This ensures the data is loaded from disk only once, on the first call, and subsequent calls retrieve the data from an in-memory cache, making the application significantly more responsive.