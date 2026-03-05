from typing import Any, Dict
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import asyncio
import shutil
import json

from fastapi.sse import EventSourceResponse


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

tasks_status: Dict[str, Dict[str, Any]] = {}  # id -> {status, progress, message, error}


async def process_pdf_task(book_id: str, file_path: Path):
    try:
        tasks_status[book_id]["status"] = "processing"
        tasks_status[book_id]["progress"] = 1

        # Transform all pages to text
        await asyncio.sleep(2)  # simulate for now
        tasks_status[book_id]["progress"] = 30
        await asyncio.sleep(3)
        tasks_status[book_id]["progress"] = 70

        tasks_status[book_id].update(
            {
                "status": "completed",
                "progress": 100,
                "result": {"pages": 42, "title": "Mon super PDF"},
            }
        )
    except Exception as e:
        tasks_status[book_id].update({"status": "failed", "error": str(e)})


@app.post("/upload")
async def upload_file(book: UploadFile, background_tasks: BackgroundTasks):
    if book.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    book_id = str(uuid.uuid4())
    file_name = f"{book_id}.pdf"
    file_path = UPLOAD_DIR / file_name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(book.file, buffer)

        tasks_status[book_id] = {
            "status": "uploaded",
            "progress": 0,
            "message": "File uploaded, please wait...",
            "error": None,
        }

        background_tasks.add_task(process_pdf_task, book_id, file_path)

    except Exception as e:
        return {"error": str(e)}

    return {"message": "File received", "id": book_id}


@app.get("/progress/{book_id}")
async def process_stream(book_id: str):
    if book_id not in tasks_status:
        raise HTTPException(404, "Unknown task")

    async def event_generator():
        while True:
            task = tasks_status.get(book_id)
            if not task:
                yield 'event: error\ndata: {"error": "Task finished or failed"}\n\n'
                return

            yield f"data: {json.dumps(task)}\n\n"

            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())
