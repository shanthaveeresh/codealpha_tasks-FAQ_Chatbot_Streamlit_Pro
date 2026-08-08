# FAQ Chatbot Pro

Professional Streamlit FAQ chatbot for Task 2.

Features:
- 38 sample FAQs
- TF-IDF + cosine similarity
- Ocean Blue, Midnight Purple and Emerald themes
- High-contrast text/input styling
- Quick questions
- Similarity confidence score
- No API key required

## Run in VS Code

```powershell
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m streamlit run app.py
```

If PowerShell blocks activation, you do not need to activate the environment.

## Deploy

Push `app.py` and `requirements.txt` to GitHub and create a Streamlit Community Cloud app with `app.py` as the main file.
