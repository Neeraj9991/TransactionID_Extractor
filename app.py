import streamlit as st
import pdfplumber
import pandas as pd
import re

st.set_page_config(page_title="Transaction ID Extractor", layout="wide")
st.title("📄 Extract Transaction Details from PDF")

uploaded_files = st.file_uploader("📤 Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    extracted_data = []
    

    for file in uploaded_files:
        try:
            with pdfplumber.open(file) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        lines = text.splitlines()

                        transaction_id = ""
                        tanker_size = ""
                        valid_from = ""
                        file_id = ""

                        for line in lines:
                            # Transaction ID
                            if "Transaction Id" in line:
                                parts = line.split(":", 1)
                                if len(parts) == 2:
                                    transaction_id = parts[1].strip()

                            # Tanker Size
                            elif "Tanker size" in line:
                                parts = line.split(":", 1)
                                if len(parts) == 2:
                                    tanker_size = parts[1].strip().split("Charges")[0].strip()

                            # Valid From
                            elif "Valid From" in line:
                                parts = line.split("-", 1)
                                if len(parts) == 2:
                                    valid_from = parts[1].strip()

                            # File Id
                            elif "File Id" in line:
                                parts = line.split("-", 1)
                                if len(parts) == 2:
                                    file_id = parts[1].strip()

                        if transaction_id:
                            extracted_data.append({
                                
                                "Transaction ID": transaction_id,
                                "Tanker Size": tanker_size,
                                "Valid From": valid_from,
                                "File Id": file_id
                            })
        except Exception as e:
            st.error(f"❌ Error reading {file.name}: {e}")

    if extracted_data:
        df = pd.DataFrame(extracted_data)
        st.success(f"✅ Extracted {len(df)} records from uploaded PDFs.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ No data extracted from the uploaded PDFs.")
else:
    st.info("Upload one or more PDF files to begin.")
