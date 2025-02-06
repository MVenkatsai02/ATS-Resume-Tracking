import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("Google_api_key"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += str(reader.pages[page].extract_text())
    return text

# Streamlit UI
st.set_page_config(page_title="Smart ATS", page_icon="📄", layout="centered")

st.title("📄 Smart ATS - Resume Evaluator")
st.write("### Optimize your resume for Applicant Tracking Systems (ATS)")

# Job description input
jd = st.text_area("🔍 Paste the Job Description", placeholder="Enter job description here...", height=150)

# Resume upload
uploaded_file = st.file_uploader("📂 Upload Your Resume (PDF)", type="pdf", help="Upload a PDF resume for evaluation")

# Submit button
if st.button("🚀 Evaluate Resume"):
    if uploaded_file is None:
        st.warning("⚠️ Please upload a resume before submitting.")
    elif not jd.strip():
        st.warning("⚠️ Job description cannot be empty.")
    else:
        with st.spinner("Processing your resume..."):
            resume_text = input_pdf_text(uploaded_file)
            
            input_prompt = f"""
            Hey, act like a skilled ATS (Applicant Tracking System) with expertise in tech fields.
            Evaluate the resume based on the given job description.
            Consider the competitive job market and provide the best suggestions for improvement.
            Assign a percentage match and identify missing keywords accurately.

            Resume: {resume_text}
            Description: {jd}

            **Response Format:**  
            - Use clear, separate sentences.  
            - Provide key insights in bullet points or numbered points.  
            - Do **not** write a long paragraph.  

            Example response:
            1. Your resume matches **XX%** of the job description.  
            2. Missing key skills: X, Y, Z.  
            3. Strengths: A, B, C.  
            4. Suggestions for improvement: D, E, F.  
            5. Consider restructuring the resume to emphasize these keywords.  
            """

            response = get_gemini_response(input_prompt)
        
        # Display results
        st.success("✅ Resume evaluation complete!")
        st.subheader("📊 ATS Evaluation Result")
        st.write(response)  # Display structured response
