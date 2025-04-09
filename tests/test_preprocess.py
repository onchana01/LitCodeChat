import unittest
import os
from src.preprocess import extract_text_from_pdf, tag_code_snippets
from src.utils import clean_text, save_text_to_file, load_text_from_file

# Real file paths
REAL_PDF_PATH = "data/raw/Python_Datascience.pdf"
TEST_OUTPUT_PATH = "data/processed/test_output.txt"

class TestPreprocess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Ensure the real PDF exists."""
        if not os.path.exists(REAL_PDF_PATH):
            raise FileNotFoundError(f"Real PDF not found at {REAL_PDF_PATH}. Please place 'Python_Datascience.pdf' in data/raw/")
        # Create a small sample output for testing
        cls.sample_text = "Intro text\nprint('Hello')\nMore text\nfor i in range(5):\n    print(i)"
        save_text_to_file(cls.sample_text, TEST_OUTPUT_PATH)

    def test_extract_text_from_pdf(self):
        """Test extracting text from the real Python_Datascience.pdf."""
        text = extract_text_from_pdf(REAL_PDF_PATH)
        self.assertTrue(len(text) > 0, "Extracted text from Python_Datascience.pdf should not be empty")
        self.assertTrue(isinstance(text, str), "Extracted text should be a string")
        # Optional: Check for Python-specific content (adjust based on your PDF)
        self.assertTrue("python" in text.lower() or "import" in text.lower(), 
                       "Expected Python-related content in extracted text")

    def test_clean_text(self):
        """Test text cleaning function with a sample."""
        raw_text = "Hello\n\n123\nWorld\n\n456"
        expected = "Hello\nWorld"
        cleaned = clean_text(raw_text)
        self.assertEqual(cleaned, expected, "Text should be cleaned of extra newlines and numbers")

    def test_tag_code_snippets(self):
        """Test tagging Python code snippets with a sample."""
        input_text = "Intro text\nprint('Hello')\nMore text\nfor i in range(5):\n    print(i)"
        expected = "Intro text\n```python\nprint('Hello')\n```\nMore text\n```python\nfor i in range(5):\n    print(i)\n```"
        tagged = tag_code_snippets(input_text)
        self.assertEqual(tagged.strip(), expected.strip(), "Code snippets should be tagged correctly")

    def test_save_and_load_text(self):
        """Test saving and loading text with a sample."""
        text = "Test content\n```python\nprint('Hi')\n```"
        save_text_to_file(text, TEST_OUTPUT_PATH)
        loaded_text = load_text_from_file(TEST_OUTPUT_PATH)
        self.assertEqual(loaded_text, text, "Loaded text should match saved text")

    @classmethod
    def tearDownClass(cls):
        """Clean up test files."""
        if os.path.exists(TEST_OUTPUT_PATH):
            os.remove(TEST_OUTPUT_PATH)

if __name__ == "__main__":
    unittest.main()