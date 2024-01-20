from dotenv import load_dotenv
load_dotenv()

import streamlit as streamlit
import os
from PIL import Image
import pdf2image 
import google.generativeai as genai

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
        pdf_parts = [{'mime_type' :"image/jpeg","data":base64.b64encode(image_byte_arr).decode()}]
        return pdf_parts
     else:
         raise FileNotFoundError("File not uploaded...")

