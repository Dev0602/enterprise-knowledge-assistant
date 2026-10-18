from pypdf import PdfReader


def load_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


if __name__ == "__main__":
    pdf_path = "data/documents/Midterm Kaggle Competition (1).pdf"

    text = load_pdf(pdf_path)

    print(text)