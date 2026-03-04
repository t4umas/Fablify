from fastapi.datastructures import UploadFile
import pdfplumber
import io


def parse_pdf(file: UploadFile):
    content = file.file.read()
    pdf = pdfplumber.open(io.BytesIO(content))
    result = []

    n = 1
    for page in pdf.pages:
        text = page.extract_text()
        cur_page = {"page": n, "content": text}
        result.append(cur_page)
        n += 1

    result.sort(key=lambda page: page["page"])
    return result
