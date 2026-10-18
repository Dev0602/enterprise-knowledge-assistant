from pathlib import Path

from src.ingestion.loader import load_pdf_pages
from src.ingestion.chunker import chunk_text
from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore


DOCUMENTS_DIR = Path("data/documents")


def ingest_documents():
    """Load PDFs, preserve page numbers, chunk, embed, and store in ChromaDB."""

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    print(f"Found {len(pdf_files)} PDF files.")

    embedder = Embedder()
    store = ChromaStore()

    total_chunks = 0

    for pdf_path in pdf_files:

        print(f"\nProcessing: {pdf_path.name}")

        pages = load_pdf_pages(str(pdf_path))

        if not pages:
            print("No text extracted from this PDF.")
            continue

        total_characters = sum(
            len(page["text"])
            for page in pages
        )

        print(
            f"Extracted {total_characters} characters "
            f"from {len(pages)} page(s)."
        )

        chunks = []
        global_chunk_index = 0

        for page in pages:

            page_chunks = chunk_text(
                text=page["text"],
                source=pdf_path.name,
            )

            for chunk in page_chunks:

                chunk["chunk_index"] = global_chunk_index
                chunk["page_number"] = page["page_number"]

                chunks.append(chunk)

                global_chunk_index += 1

        print(f"Created {len(chunks)} chunks.")

        if not chunks:
            continue

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:

            chunk_id = (
                f"{pdf_path.stem}_"
                f"p{chunk['page_number']}_"
                f"c{chunk['chunk_index']}"
            )

            embedding = embedder.embed(
                chunk["text"]
            )

            ids.append(chunk_id)
            documents.append(chunk["text"])
            embeddings.append(embedding)

            metadatas.append(
                {
                    "source": chunk["source"],
                    "page_number": chunk["page_number"],
                    "chunk_index": chunk["chunk_index"],
                    "start_char": chunk["start_char"],
                    "end_char": chunk["end_char"],
                }
            )

        store.add_documents(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        total_chunks += len(chunks)

        print(f"Stored {len(chunks)} chunks.")

    print("\n" + "=" * 50)
    print("INGESTION COMPLETE")
    print("=" * 50)

    print(f"PDF files processed: {len(pdf_files)}")
    print(f"Total chunks added: {total_chunks}")
    print(
        f"Chroma collection size: "
        f"{store.collection.count()}"
    )


if __name__ == "__main__":
    ingest_documents()
