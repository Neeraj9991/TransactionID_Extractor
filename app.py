import streamlit as st
import pdfplumber
import pandas as pd
import re

st.set_page_config(page_title="Transaction ID Extractor", layout="wide")
st.title("📄 Extract Transaction IDs from PDF")

uploaded_files = st.file_uploader("📤 Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    extracted_data = []

    for file in uploaded_files:
        try:
            # Try to extract date using regex like 'DD.MM.YY'
            date_match = re.search(r"\b(\d{2}\.\d{2}\.\d{2})\b", file.name)
            extracted_date = date_match.group(1) if date_match else "Not found"

            with pdfplumber.open(file) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        for line in text.splitlines():
                            if "Transaction Id" in line:
                                parts = line.split(":")
                                if len(parts) == 2:
                                    transaction_id = parts[1].strip()
                                    extracted_data.append({
                                        "File Name": file.name,
                                        "Date from File": extracted_date,
                                        "Page": i + 1,
                                        "Transaction ID": transaction_id
                                    })
        except Exception as e:
            st.error(f"❌ Error reading {file.name}: {e}")

    if extracted_data:
        df = pd.DataFrame(extracted_data)
        st.success(f"✅ Extracted {len(df)} transaction IDs.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No transaction IDs extracted.")
else:
    st.info("Upload one or more PDF files to begin.")
