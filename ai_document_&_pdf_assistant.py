
import streamlit as st
import google.generativeai as genai
import pypdf

st.set_page_config(page_title="AI Document Assistant", layout="wide")

st.title("📄 AI Document & PDF Assistant")
st.write("Upload your PDF files and ask any questions based on their content!")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is not None:
    pdf_reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    st.success(f"PDF uploaded successfully! Total pages: {len(pdf_reader.pages)}")

    user_query = st.text_input("Ask a question about your PDF:")

    if st.button("Get Answer"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar.")
        else:
            try:
                genai.configure(api_key=api_key.strip())
                prompt = f"Context from PDF document:\n{text}\n\nQuestion: {user_query}\nAnswer:"

                with st.spinner("Analyzing document..."):
                    model = genai.GenerativeModel('gemini-3.6-flash')
                    response = model.generate_content(prompt)
                    st.write("### Answer:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
