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

    pages = split_book_into_pages(source_file)

    write_pages(book_dir, pages)


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


def split_book_into_pages(source_file: Path):
    result = []
    with pdfplumber.open(source_file) as pdf:
        for n, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            result.append({"page": n, "content": text})

    return result


def write_pages(book_dir: Path, pages: list[Dict]):
    pages_dir = book_dir / "pages"
    pages_dir.mkdir()
    for page in pages:
        page_file = pages_dir / f"page_{page['page']}.txt"
        page_file.write_text(page["content"] or "", encoding="utf-8")

