from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import NamedTemporaryFile
app = FastAPI()

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        #returns transcription
        return JSONResponse(content={"transcription": file_location})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"


