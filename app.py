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
st.header("ATS Resume Matching and Creating Resume")

# input
input = st.text_area("Enter Job Descrition", key='input')
uplaoded_file =  st.file_uploader("Upload your resume here must be in pdf format", type=['pdf'])

if uplaoded_file is not None:
    st.write("You have successfully uploaded your file...")
    submit_btn_1 = st.button("Tell me about the resume")
    submit_btn_2 = st.button("How can I prove my skills")
    submit_btn_4 = st.button("Percentage match")
    input_prompt1 = """
        You are an experienced HR with Tech Experience in the field of data science, full stack web development, AI, Big Data Engineering, DevOps, data analyst
        your task is to review the provided resume against the job description for these profiles. 
        Please share your professional evaluation on whether the candidate's profile aligns with the role. 
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """
    # input_prompt3 = """
    #     You are an Technical Human Resource Manager with experience in data science, full stack web development, AI, Big Data Engineering, DevOps, data analyst.
    #     Your role is to scrutinize the resume in the light of the job description provided. 
    #     Share your insight on the candidate's suitability for the role from HR perspective.
    #     Additionally, offer advice on ehancing candidate's skill
    #     """

    input_prompt3 = """
        You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science , full stack web development, AI, Big Data Engineering, DevOps, data analyst and deep ATS functionality, 
        your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
        the job description. First the output should come as percentage and then keywords missing and last final thoughts.
        """
    
    if submit_btn_1:
        if uplaoded_file is not None:
            pdf_content = input_pdf_setup(uplaoded_file)
            response = get_gemini_response(input,pdf_content,input_prompt1)
            st.subheader("Response:")
            st.write(response)
        else:
            st.write("please upload resume..")

    elif submit_btn_2:
        if uplaoded_file is not None:
            pdf_content = input_pdf_setup(uplaoded_file)
            response = get_gemini_response(input,pdf_content,input_prompt3)
            st.subheader("Response:")
            st.write(response)
        else:
            st.write("please upload resume..")
