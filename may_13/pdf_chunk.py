import fitz

def extract_pdf_text(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

if __name__ == "__main__":
    text = extract_pdf_text("sample.pdf")
    chunks = chunk_text(text)
    for idx, chunk in enumerate(chunks):
        print(f"\n--- Chunk {idx+1} ---\n{chunk[:300]}...")
