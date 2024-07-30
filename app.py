from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import NamedTemporaryFile
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv, dotenv_values 
from botocore.client import Config
import ollama 
import httpx
import PyPDF2


app = FastAPI()

load_dotenv()

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
        response = ollama.chat(model='llama3', messages=[
            {
                "role": "user", 
                "content": 'The following text is an applicant\'s resume. You must sort it and summarize it into the following categories: years of experience, skills, experiences, projects, awards. Your output should have a very brief format, with the total years of experience listed after "Years of Experience." The list of skills should be listed after "Skills." The list of experiences with brief descriptions should be listed after "Experiences." The list of projects with brief descriptions should be listed after "Projects." A list of the awards should be given after "Awards." Nothing else should be output. Don\'t give any introduction before giving this output, all I need is this output and nothing else. You must include all the fields I mentioned and label them as I specified. If you cannot find information for any of these fields, label it n/a. Here is the resume: ' + text,

            },
        ])
        return response['message']['content']
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
                        endpoint_url = os.getenv('endpoint'), 
                        region_name = 'nyc3',
                        aws_access_key_id = os.getenv('ACCESS_KEY_ID'),
                        aws_secret_access_key = os.getenv('SECRET_ACCESS_KEY'))

if not os.path.exists('temp'):
    os.makedirs('temp')


@app.post("/transcribe/")
async def transcribe_audio(filekey: str):
    try:
        file_location = f"temp/{filekey}"
        try:
            client.download_file(os.getenv('Bucket'), filekey, file_location)
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise HTTPException(status_code=403, detail="Credentials error")

        extracted = extract_text_from_pdf(file_location)

        os.remove(file_location)

        insights = summarize_resume(extracted)

        client.put_object(Bucket = os.getenv('Bucket'), Key = filekey + ' Summary', Body = insights)

        #returns transcription
        return JSONResponse(content={"transcription": "Summary Uploaded Succesfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"


