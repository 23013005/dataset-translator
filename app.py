import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from time import sleep

st.set_page_config(
    page_title="Dataset Translator ID → EN",
    layout="centered"
)

st.title("📊 Dataset Translator: Indonesian → English")
st.caption("Upload CSV → Translate kolom → Download hasil")

uploaded_file = st.file_uploader(
    "Upload file CSV (dataset bahasa Indonesia)",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview Dataset")
    st.dataframe(df.head(10))

    column = st.selectbox(
        "Pilih kolom yang berisi bahasa Indonesia",
        df.columns
    )

    if st.button("Translate Dataset"):
        translator = GoogleTranslator(source="id", target="en")

        translated = []

        progress = st.progress(0)
        total = len(df)

        for i, text in enumerate(df[column]):
            try:
                if pd.isna(text) or str(text).strip() == "":
                    translated.append("")
                else:
                    translated.append(translator.translate(str(text)))
                sleep(0.1)
            except Exception:
                translated.append("")
            
            progress.progress((i + 1) / total)

        df[f"{column}_english"] = translated

        st.success("Translasi selesai")

        st.subheader("Preview Hasil")
        st.dataframe(df.head(10))

        st.download_button(
            label="Download CSV Hasil",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="translated_dataset.csv",
            mime="text/csv"

        )
