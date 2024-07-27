from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import NamedTemporaryFile
import whisperx
import torch
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}