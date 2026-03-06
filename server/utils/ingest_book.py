import json
from pathlib import Path
from typing import Any, Dict
import pdfplumber
from storage import BOOKS_DIR


def ingest_book(book_id: str, source_file: Path):
    metadata = parse_book_metadata(source_file)

    if metadata is None:
        raise ValueError(f"Impossible d'extraire les metadata du PDF : {source_file}")

    book_dir = create_book_dir(book_id)
    write_metadata(book_dir, metadata)


# Create book directory + create metadas
# Turn book into pages
# Write pages


def parse_book_metadata(book_file: Path):
    # => {
    #   title,
    #   author,
    #   pages,
    # }
    try:
        with pdfplumber.open(book_file) as pdf:
            meta = pdf.metadata
            page_count = len(pdf.pages)

            info = {
                "title": meta.get("Title"),
                "author": meta.get("Author"),
                "pages": page_count,
            }

        return info
    except Exception as e:
        print("PDF error : ", e)
        return None


def create_book_dir(book_id: str):
    book_path = BOOKS_DIR / book_id
    book_path.mkdir(parents=True)
    return book_path


def write_metadata(book_dir: Path, metadata: Dict[str, Any]):
    metadata_file = book_dir / "metadata.json"
    metadata_str = json.dumps(metadata, indent=4, ensure_ascii=False)
    with open(metadata_file, "w", encoding="utf-8") as f:
        f.write(metadata_str)

