from fastapi import FastAPI, File, UploadFile, HTTPException


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}