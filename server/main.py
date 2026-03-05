from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import shutil


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a directory for uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload")
def upload_file(book: UploadFile = File(...)):
    if book.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    id = uuid.uuid4()
    file_name = f"{id}.pdf"
    file_path = UPLOAD_DIR / file_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(book.file, buffer)
        book.file.close()
    except Exception as e:
        return {"error": str(e)}

    return {"message": "File received", "id": id}
