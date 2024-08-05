from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses  import JSONResponse, RedirectResponse
#from tempfile import NamedTemporaryFile, TemporaryDirectory
import os
#import boto3
#from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
#from botocore.client import Config
#import httpx
#import PyPDF2
#import google.generativeai as genai

app = FastAPI()

load_dotenv()

@app.post("/transcribe/")
async def root():
    key = os.getenv('GEMINI_API_KEY')
    if not key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set")

    return JSONResponse(content={"transcription": "Summary Successfully Created"})

@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"




"""
key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-flash')


def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"An error occurred while extracting text from the PDF: {e}")
        return None
    

def summarize_resume(text):
    try:
        response = model.generate_content(
            
            'The following text is an applicant\'s resume. You must sort it and summarize it into the following categories: years of experience, skills, experiences, projects, awards. Your output should have a very brief format, with the total years of experience listed after "Years of Experience." The list of skills should be listed after "Skills." The list of experiences with brief descriptions should be listed after "Experiences." The list of projects with brief descriptions should be listed after "Projects." A list of the awards should be given after "Awards." Nothing else should be output. Don\'t give any introduction before giving this output, all I need is this output and nothing else. You must include all the fields I mentioned and label them as I specified. If you cannot find information for any of these fields, label it n/a. Here is the resume:' + text,

        )
        return response.text
    except httpx.RequestError as e:
        print(f"An HTTP request error occurred: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"An HTTP status error occurred: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while summarizing the resume: {e}")
        return None
    
session = boto3.session.Session()
client = session.client('s3',
                        endpoint_url=os.getenv('endpoint'), 
                        region_name='nyc3',
                        aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))

@app.post("/transcribe/")
async def transcribe_audio(filekey: str):
    with TemporaryDirectory() as temp_dir:
        file_location = os.path.join(temp_dir, filekey)
        try:
            client.download_file(os.getenv('Bucket'), filekey, file_location)
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise HTTPException(status_code=403, detail="Credentials error")

        extracted = extract_text_from_pdf(file_location)
        if extracted is None:
            raise HTTPException(status_code=500, detail="Failed to extract text from PDF")

        
        insights = summarize_resume(extracted)
        if insights is None:
            raise HTTPException(status_code=500, detail="Failed to summarize resume")
      

        client.put_object(Bucket=os.getenv('Bucket'), Key=filekey + ' Summary', Body=insights)

        return JSONResponse(content={"transcription": "Summary Successfully Created"})

@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"
"""