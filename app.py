import streamlit as st
import pandas as pd
from main import summarize

st.title("📄 Text Summarization")
st.markdown("Menggunakan algoritma **TF-IDF** + **Cosine Similarity** (implementasi manual)")

uploaded_file = st.file_uploader("Upload file .md", type=["md"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")

    st.subheader("📌 Original Text")
    st.text_area("Isi Dokumen", content, height=200, disabled=True)

    top_n = st.slider("Jumlah Kalimat Ringkasan per Paragraf", 1, 5, 2)

    if st.button("🔍 Generate Summary"):
        result = summarize(content, top_n)

        st.subheader("📝 Hasil Summary")

        # Pisahkan hasil yang punya skor dan yang tidak
        scored     = [r for r in result if r["skor"] is not None]
        unscored   = [r for r in result if r["skor"] is None]

        # Tabel kalimat dengan skor TF-IDF
        if scored:
            st.markdown("#### tabel Skor Cosine Similarity (TF-IDF)")
            df = pd.DataFrame(scored)
            df.columns = ["Kalimat", "Skor Cosine Similarity"]
            df_sorted = df.sort_values("Skor Cosine Similarity", ascending=False).reset_index(drop=True)
            df_sorted.index = df_sorted.index + 1  # ranking mulai dari 1
            st.dataframe(df_sorted, use_container_width=True)

        # Kalimat tanpa skor (paragraf pendek, langsung diambil semua)
        if unscored:
            st.markdown("#### 📋 Kalimat Langsung (paragraf pendek)")
            for i, r in enumerate(unscored, 1):
                st.write(f"{i}. {r['kalimat']}")

        # Ringkasan akhir dalam urutan asli
        st.markdown("---")
        st.subheader("Ringkasan Akhir")
        for r in result:
            st.markdown(f"- {r['kalimat']}")