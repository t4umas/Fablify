from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from utils import parsePDF


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Message": "Please select a route"}


@app.post("/upload")
def upload_file(book: UploadFile = File(...)):
    if book.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Convert pdf into text
    result = parsePDF.parse_pdf(book)
    if not result:
        raise HTTPException(status_code=400, detail="Could not parse pdf")

    return {"message": "File received", "result": result}
