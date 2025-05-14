import fitz  # PyMuPDF

def extract_pdf_text(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Test it
if __name__ == "__main__":
    filepath = "sample_text.pdf"
    output = extract_pdf_text(filepath)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(output)
