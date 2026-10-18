from pathlib import Path

from src.ingestion.loader import load_pdf
from src.ingestion.chunker import chunk_text
from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore


DOCUMENTS_DIR = Path("data/documents")


def ingest_documents():
    """Load PDFs, chunk text, create embeddings, and store them in ChromaDB."""

    # 1. Find all PDF files
    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    print(f"Found {len(pdf_files)} PDF files.")

    # 2. Initialize embedding model and ChromaDB
    embedder = Embedder()
    store = ChromaStore()

    total_chunks = 0

    # 3. Process each PDF
    for pdf_path in pdf_files:

        print(f"\nProcessing: {pdf_path.name}")

        # Load PDF text
        text = load_pdf(str(pdf_path))

        if not text:
            print("No text extracted from this PDF.")
            continue

        print(f"Extracted {len(text)} characters.")

        # Chunk the text
        chunks = chunk_text(
            text=text,
            source=pdf_path.name,
        )

        print(f"Created {len(chunks)} chunks.")

        if not chunks:
            continue

        # Prepare data for ChromaDB
        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:

            chunk_id = f"{pdf_path.stem}_{chunk['chunk_index']}"

            embedding = embedder.embed(chunk["text"])

            ids.append(chunk_id)
            documents.append(chunk["text"])
            embeddings.append(embedding)

            metadatas.append(
                {
                    "source": chunk["source"],
                    "chunk_index": chunk["chunk_index"],
                    "start_char": chunk["start_char"],
                    "end_char": chunk["end_char"],
                }
            )

        # Store everything in ChromaDB
        store.add_documents(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        total_chunks += len(chunks)

        print(f"Stored {len(chunks)} chunks.")

    # 4. Final summary
    print("\n" + "=" * 50)
    print("INGESTION COMPLETE")
    print("=" * 50)

    print(f"PDF files processed: {len(pdf_files)}")
    print(f"Total chunks added: {total_chunks}")
    print(f"Chroma collection size: {store.collection.count()}")


if __name__ == "__main__":
    ingest_documents()