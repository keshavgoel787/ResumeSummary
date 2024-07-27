from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}