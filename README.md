# MedIntel AI

MedIntel AI is a medical report analysis backend scaffold designed to support OCR, clinical parsing, abnormality detection, risk prediction, summarization, and RAG-powered retrieval.

## Structure

- `app.py` - backend entry point
- `requirements.txt` - Python dependencies
- `.env` - environment variable placeholders
- `data/` - data storage folders
- `modules/` - feature modules for OCR, parsing, analysis, summarization, and RAG
- `assets/` - static assets and screenshots
- `tests/` - test folder

## Running the project

1. Create a Python virtual environment and activate it:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Start the backend in one terminal:

   ```powershell
   python app.py
   ```

4. Start the Streamlit frontend in another terminal:

   ```powershell
   streamlit run streamlit_app.py
   ```

5. Open the Streamlit app in your browser at the URL shown by Streamlit (usually `http://localhost:8501` or `http://localhost:8502`).

6. Upload a PDF and click **Process & Extract**.
