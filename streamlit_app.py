pip install PyPDF2
import streamlit as st
import PyPDF2
import os

# Ensure there's a folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_pdf_to_text(file_path):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page in range(reader.numPages):
            text += reader.getPage(page).extractText()
        return text

# Add a section in your Streamlit UI for resume upload
with st.sidebar:
    st.header("Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a file", type='pdf')
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Convert the uploaded PDF to text
        resume_text = convert_pdf_to_text(file_path)
        st.success('File uploaded successfully')
        st.text_area("Extracted Text", resume_text, height=300)


