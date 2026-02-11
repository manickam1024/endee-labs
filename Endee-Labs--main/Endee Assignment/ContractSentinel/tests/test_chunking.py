import unittest
from backend.ingestion.chunking import RecursiveTokenChunker

class TestRecursiveTokenChunker(unittest.TestCase):
    def setUp(self):
        self.chunker = RecursiveTokenChunker(chunk_size=50, chunk_overlap=10)

    def test_simple_split(self):
        text = "This is a short text."
        chunks = self.chunker.split_text(text)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], text)

    def test_long_text_split(self):
        # Create a text longer than 50 chars
        text = "A" * 60
        chunks = self.chunker.split_text(text)
        self.assertTrue(len(chunks) > 1)
        # Check that no chunk exceeds the limit (roughly, our simple implementation might be soft on this)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 50)

    def test_separator_priority(self):
        text = "Sentence one. Sentence two. Sentence three."
        # Should split by '. ' rather than strictly char count if possible
        chunks = self.chunker.split_text(text)
        self.assertTrue(any("Sentence one." in c for c in chunks))

if __name__ == '__main__':
    unittest.main()
