DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict]:
    """Split text into overlapping chunks with source metadata."""
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be less than chunk_size")

    if not text:
        return []

    chunks: list[dict] = []
    step = chunk_size - chunk_overlap
    start = 0
    chunk_index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_body = text[start:end].strip()

        if chunk_body:
            chunks.append(
                {
                    "text": chunk_body,
                    "source": source,
                    "chunk_index": chunk_index,
                    "start_char": start,
                    "end_char": end,
                }
            )
            chunk_index += 1

        if end >= len(text):
            break

        start += step

    return chunks
