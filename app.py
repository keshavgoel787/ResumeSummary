from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import NamedTemporaryFile

app = FastAPI()

@app.post("/transcribe/")

@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"