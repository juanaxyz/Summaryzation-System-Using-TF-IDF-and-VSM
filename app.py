import streamlit as st
from main import summarize

st.title("📄 Text Summarization")

uploaded_file = st.file_uploader("Upload file .md", type=["md"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")

    st.subheader("📌 Original Text")
    st.write(content)

    top_n = st.slider("Jumlah kalimat", 1, 5, 2)

    if st.button("Generate Summary"):
        result = summarize(content, top_n)
        st.write("debug: ", result)

        st.subheader("📝 Summary")
        for r in result:
            st.write("- " + r)