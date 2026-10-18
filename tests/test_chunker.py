import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ingestion.chunker import chunk_text


class TestChunker(unittest.TestCase):
    SOURCE = "data/documents/example.pdf"

    def test_empty_text_returns_no_chunks(self):
        self.assertEqual(chunk_text("", self.SOURCE), [])

    def test_short_text_returns_single_chunk(self):
        text = "hello world"
        chunks = chunk_text(text, self.SOURCE)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["text"], text)
        self.assertEqual(chunks[0]["source"], self.SOURCE)
        self.assertEqual(chunks[0]["chunk_index"], 0)
        self.assertEqual(chunks[0]["start_char"], 0)
        self.assertEqual(chunks[0]["end_char"], len(text))

    def test_normal_text_creates_multiple_fixed_size_chunks(self):
        text = "a" * 2500
        chunks = chunk_text(text, self.SOURCE)

        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0]["start_char"], 0)
        self.assertEqual(chunks[0]["end_char"], 1000)
        self.assertEqual(chunks[1]["start_char"], 800)
        self.assertEqual(chunks[1]["end_char"], 1800)
        self.assertEqual(chunks[-1]["end_char"], 2500)

        for index, chunk in enumerate(chunks):
            self.assertEqual(chunk["source"], self.SOURCE)
            self.assertEqual(chunk["chunk_index"], index)
            self.assertEqual(chunk["text"], text[chunk["start_char"] : chunk["end_char"]])

    def test_overlapping_chunks_share_boundary_text(self):
        text = "abcdefghijklmnopqrstuvwxyz" * 100  # 2600 characters
        chunks = chunk_text(text, self.SOURCE)

        self.assertGreaterEqual(len(chunks), 2)

        first = chunks[0]
        second = chunks[1]

        overlap_start = second["start_char"]
        overlap_end = first["end_char"]

        self.assertEqual(overlap_end - overlap_start, 200)
        self.assertEqual(
            text[overlap_start:overlap_end],
            text[first["start_char"] : first["end_char"]][-200:],
        )
        self.assertEqual(
            text[overlap_start:overlap_end],
            text[second["start_char"] : second["end_char"]][:200],
        )


if __name__ == "__main__":
    unittest.main()
