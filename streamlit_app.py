import streamlit as st
from utilities.AI_API import *
import PyPDF2
import os
import re

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

def generate_summary(resume_text):
    # Placeholder function for generating a summary
    # Implement more complex logic as needed
    return "This is a placeholder summary."

def identify_strengths_weaknesses(resume_text):
    # Placeholder function for identifying strengths and weaknesses
    # Implement more complex logic as needed
    strengths = "Placeholder strengths"
    weaknesses = "Placeholder weaknesses"
    return strengths, weaknesses

def extract_skills(resume_text):
    # Define a list of skills to look for
    skill_set = {"Python", "Java", "C++", "JavaScript", "SQL", "React", "Node.js", "HTML", "CSS", "AWS", "Docker", "Kubernetes", "Machine Learning", "Deep Learning"}

    # Find these skills in the resume text
    found_skills = set()
    for skill in skill_set:
        if skill.lower() in resume_text.lower():
            found_skills.add(skill)
    return list(found_skills)

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

        # Analyze the resume
        summary = generate_summary(resume_text)
        strengths, weaknesses = identify_strengths_weaknesses(resume_text)
        skills = extract_skills(resume_text)

        # Display the analysis results
        st.subheader("Resume Analysis")
        st.text_area("Summary", summary, height=100)
        st.text_area("Strengths", strengths, height=100)
        st.text_area("Weaknesses", weaknesses, height=100)
        st.multiselect("Skills Extracted", skills, default=skills)

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


