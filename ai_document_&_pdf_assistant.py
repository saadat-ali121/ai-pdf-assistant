
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
       
             if st.button("Submit & Process"):
            with st.spinner("Processing...")
                available_models = [
                    'gemini-1.5-flash',
                    'gemini-1.5-pro',
                    'gemini-2.0-flash'
                ]

                response = None
                last_error = None

                for model_name in available_models:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(prompt)
                        if response:
                            break
                    except Exception as err:
                        last_error = err
                        continue

                if response:
                    st.write("### Answer:")
                    st.write(response.text)
                else:
                    st.error(f"Models temporarily unavailable: {last_error}")   try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    if response:
                        break  # Agar response mil jaye toh loop ruk jaye ga
                except Exception as err:
                    last_error = err
                    continue  # Agar ek model fail ho toh agla try kare ga

            if response:
                st.write("### Answer:")
                st.write(response.text)
            else:
                st.error(f"Models temporarily unavailable: {last_error}")
