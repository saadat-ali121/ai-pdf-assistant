import streamlit as st
import google.generativeai as genai
import pypdf

st.set_page_config(page_title="AI Document Assistant", layout="wide")

st.title("📄 AI Document & PDF Assistant")
st.write("Upload your PDF files and ask any questions based on their content!")

# 1. API Key Setup
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)

# 2. Session State for Text Persistence
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is not None:
    pdf_reader = pypdf.PdfReader(uploaded_file)
    extracted = ""
    for page in pdf_reader.pages:
        t = page.extract_text()
        if t:
            extracted += t + "\n"
    
    st.session_state.extracted_text = extracted
    st.success(f"PDF uploaded successfully! Total pages: {len(pdf_reader.pages)}")

# 3. User Input & Processing
user_query = st.text_input("Ask a question about your PDF:")

if st.button("Get Answer"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar first!")
    elif not st.session_state.extracted_text:
        st.warning("Please upload a PDF document first!")
    elif not user_query:
        st.warning("Please enter a question first!")
    else:
        with st.spinner("Processing..."):
            # Context and Query Combination
            full_prompt = f"""
            You are a helpful assistant. Answer the user's question based strictly on the context provided below.
            
            Context from PDF:
            {st.session_state.extracted_text}
            
            User Question:
            {user_query}
            """

           available_models = [
    'models/gemini-1.5-flash',
    'models/gemini-1.5-pro',
    'models/gemini-2.0-flash-exp',
    'models/gemini-1.5-flash-8b'
]
            response = None
            last_error = None

            for model_name in available_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(full_prompt)
                    if response and response.text:
                        break
                except Exception as err:
                    last_error = err
                    continue

            if response and response.text:
                st.write("### Answer:")
                st.write(response.text)
            else:
                st.error(f"Error calling Gemini API: {last_error}")
