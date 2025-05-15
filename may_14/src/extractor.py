import PyPDF2
from db import Chunk

def extract_text(pdf_path: str) -> list:
    reader = PyPDF2.PdfReader(pdf_path)
    chunks = []
    
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            chunks.append(Chunk(
                text=text,
                source=pdf_path,
                page=page_num + 1
            ))
    
    return chunks