import streamlit as st
import boto3
from utilities.AI_API import *
import os
import re

#Ensure there's a folder to save uploaded files
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

# Function to upload a file to an S3 bucket
def upload_to_s3(file_name, bucket_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket_name, file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
        
def analyze_resume(resume_text):
    # Use the functions from your AI API
    summary = generate_summary(resume_text)
    strengths = identify_strengths(resume_text)
    weaknesses = identify_weaknesses(resume_text)
    return summary, strengths, weaknesses

def extract_skills(resume_text):
    # Define a list of skills to look for
    skill_set = {"Python", "Java", "C++", "JavaScript", "SQL", "React", "Node.js", "HTML", "CSS", "AWS", "Docker", "Kubernetes", "Machine Learning", "Deep Learning"}

    # Find these skills in the resume text
    found_skills = set()
    for skill in skill_set:
        if skill.lower() in resume_text.lower():
            found_skills.add(skill)
    return list(found_skills)

# Streamlit UI
st.header("Resume Analysis Tool")

with st.sidebar:
    st.header("Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a file", type='pdf')
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Upload file to S3
        if upload_to_s3(file_path, 'your-s3-bucket-name'):
            st.success('File uploaded to S3 successfully')

        # Convert the uploaded PDF to text
        resume_text = convert_pdf_to_text(file_path)

        # Analyze the resume using your AI API
        summary, strengths, weaknesses = analyze_resume(resume_text)

        # Display the analysis results
        st.subheader("Resume Analysis")
        st.text_area("Summary", summary, height=100)
        st.text_area("Strengths", strengths, height=100)
        st.text_area("Weaknesses", weaknesses, height=100)


