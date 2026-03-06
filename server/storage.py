from pathlib import Path

DATA_DIR = Path("data")

UPLOAD_DIR = DATA_DIR / "uploads"
BOOKS_DIR = DATA_DIR / "books"


def init_storage():
    for path in [DATA_DIR, UPLOAD_DIR, BOOKS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
