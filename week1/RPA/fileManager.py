import streamlit as st
import os
from pathlib import Path
from datetime import datetime

# ---------- Setup ----------
BASE_DIR = Path("marvel_uploaded_files")
BASE_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Marvel File Manager", layout="centered", page_icon="🦸‍♂️")

# ---------- Marvel UI CSS ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Anton&display=swap');

    html, body, .stApp {
        background-color: #0d0d0d;
        color: white;
        font-family: 'Anton', sans-serif;
    }

    h1 {
        font-size: 3.5em;
        color: #e62429;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 10px;
        margin-top: 5px;
    }

    .marvel-header {
        background: linear-gradient(to right, #e62429, #111);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        color: white;
        margin-bottom: 1rem;
    }

    .stTextInput input {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #e62429;
        border-radius: 10px;
    }

    .stButton > button {
        background-color: #e62429;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        padding: 0.4rem 1.2rem;
        border: none;
    }

    .stDownloadButton > button {
        background-color: #202020;
        color: white;
        border-radius: 8px;
        padding: 0.4rem 1rem;
    }

    .file-card {
        background-color: #1a1a1a;
        border: 1px solid #e62429;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 12px;
    }

    .footer {
        margin-top: 2rem;
        text-align: center;
        font-size: 0.8rem;
        color: #aaa;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("# MARVEL FILE MANAGER 🦸‍♂️")

# ---------- Upload ----------
uploaded_files = st.file_uploader("📤 Upload File(s)", type=None, accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        (BASE_DIR / file.name).write_bytes(file.read())
    st.success("File(s) uploaded successfully!")

# ---------- Search ----------
search_query = st.text_input("🔎 Search files by name:")

# ---------- File Listing ----------
st.markdown("### 🧾 Stored Files")

files = sorted(BASE_DIR.glob("*"), key=os.path.getmtime, reverse=True)
filtered = [f for f in files if search_query.lower() in f.name.lower()]

if not filtered:
    st.info("No matching files found.")
else:
    for f in filtered:
        with st.container():
            st.markdown(f"""
                <div class="file-card">
                    <b>📎 {f.name}</b><br>
                    <span style="font-size:0.85em;">🗂️ {round(f.stat().st_size / 1024, 2)} KB • ⏱️ {datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}</span><br><br>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 1])
            with open(f, "rb") as fdata:
                col1.download_button("⬇️ Download", fdata.read(), file_name=f.name)
            if col2.button("🗑️ Delete", key=f"del_{f.name}"):
                f.unlink()
                st.warning(f"{f.name} deleted.")
                st.experimental_rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ---------- Create Folder ----------
st.markdown("### 🏗️ Create Folder")
folder_name = st.text_input("New folder name")

if st.button("➕ Create"):
    new_path = BASE_DIR / folder_name
    try:
        new_path.mkdir()
        st.success(f"Folder '{folder_name}' created.")
    except FileExistsError:
        st.warning("Folder already exists.")
    except Exception as e:
        st.error(str(e))

# ---------- Footer ----------
st.markdown('<div class="footer">© 2025 Marvel UI File Manager by ChatGPT</div>', unsafe_allow_html=True)
