from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import NamedTemporaryFile

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}