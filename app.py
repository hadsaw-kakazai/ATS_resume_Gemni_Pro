from dotenv import load_dotenv
load_dotenv()
import io
import base64
import streamlit as st
import os
from PIL import Image
import pdf2image 
import google.generativeai as genai
from pdf2image import convert_from_path

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# funcation to get response from API
def get_gemini_response(input, pdf_content,prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, pdf_content[0],prompt])
    return response.text


def input_pdf_setup(file):
     if file is not None:
        images = pdf2image.convert_from_bytes(file.read())
        firstpage = images[0]
        image_byte_arr = io.BytesIO()
        firstpage.save(image_byte_arr,  format="JPEG")
        image_byte_arr = image_byte_arr.getvalue()
        pdf_parts = [
            {'mime_type' :"image/jpeg",
             "data":base64.b64encode(image_byte_arr).decode()
             
             }
            ] 
        return pdf_parts
     else:
         raise FileNotFoundError("File not uploaded...")
     

# Creating frontend part
     
st.set_page_config(page_title = "ATS Resume with Gemini Pro Vision")
st.header("ATS Resume Checker")

# input
input = st.text_area("Enter Job Descrition", key='input')
uplaoded_file =  st.file_uploader("Upload your resume here must be in pdf format", type=['pdf'])

if uplaoded_file is not None:
    st.write("You have successfully uploaded your file...")
    submit_btn_1 = st.button("Tell me about my resume")
    submit_btn_2 = st.button("How can I prove my skills")
    submit_btn_3 = st.button("Percentage match")
    input_prompt1 = """
        You are an experienced HR with Tech Experience in different fields.
        your task is to review the provided resume against the job description and tell me is I am a good fit for this job position.
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements in bullet points.
        """
    input_prompt2 = """
        You are an experienced ATS (Applicant Tracking System) and resume checker.
        You need to extract the skills from the job description.
        You must tell the candidate what skills are missing in the resume and how and where he/she can improve the skills,
        also share the links where he/she can learn those missing skils
        """

    input_prompt3 = """
You are an experienced ATS (Applicant Tracking System) scanner with an in-depth understanding of ATS functionality. Your goal is to develop a system that extracts keywords or skills from a candidate's resume and matches them with a given job description. The output should be presented in the following format:

Percentage Match:

Generate a percentage indicating the match between the candidate's resume and the job description based on the extracted keywords or skills.
Keywords Missing:

Identify and list the keywords or skills from the job description that are missing in the candidate's resume.
Final Thoughts:

Provide a summary or analysis of the overall compatibility between the candidate and the job based on the keyword matching process.
Visualization:

Create a chart for better visualization of the keyword matching results. You may consider using a chart to display the match percentage and highlight the missing keywords.
Example Input:

Candidate's Resume: [Input text]
Job Description: [Input text]

Example Output:

Percentage Match: 75%
Keywords Missing: [List of missing keywords]
Final Thoughts: The candidate demonstrates a strong match with the job requirements, but improvements can be made by incorporating the missing keywords.

Ensure the generated output is clear, concise, and effectively communicates the match analysis between the candidate's resume and the job description.
        """
    
    if submit_btn_1:
        if uplaoded_file is not None:
            pdf_content = input_pdf_setup(uplaoded_file)
            response = get_gemini_response("Job Description"+input,pdf_content,input_prompt1)
            st.subheader("Response:")
            st.write(response)
        else:
            st.write("please upload resume..")

    elif submit_btn_3:
        if uplaoded_file is not None:
            pdf_content = input_pdf_setup(uplaoded_file)
            response = get_gemini_response("Job Description"+input,pdf_content,input_prompt3)
            st.subheader("Response:")
            st.write(response)
        else:
            st.write("please upload resume..")

    elif submit_btn_2:
        if uplaoded_file is not None:
            pdf_content = input_pdf_setup(uplaoded_file)
            response = get_gemini_response("Job Description"+input,pdf_content,input_prompt2)
            st.subheader("Response:")
            st.write(response)
        else:
            st.write("please upload resume..")
