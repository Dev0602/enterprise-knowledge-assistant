from pypdf import PdfReader


def load_pdf_pages(file_path: str) -> list[dict]:
    """Extract text from a PDF while preserving page numbers."""
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text and page_text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": page_text,
                }
            )

    return pages


def load_pdf(file_path: str) -> str:
    """
    Extract all PDF text as one string.

    Kept for backward compatibility with existing tests/code.
    """
    pages = load_pdf_pages(file_path)

    return "\n".join(
        page["text"]
        for page in pages
    )
