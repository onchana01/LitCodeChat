import re
import os
from pdfminer.high_level import extract_text

# Paths
RAW_BOOK_PATH = "data/raw/Python_Datascience.pdf"
OCR_OUTPUT_PATH = "data/processed/ocr_output.pdf"
PROCESSED_TEXT_PATH = "data/processed/book_text.txt"

def extract_text_from_pdf(pdf_path):
    """Extract text from the OCR'd PDF using pdfminer.six."""
    if not os.path.exists(pdf_path):
        print(f"PDF file not found at: {pdf_path}")
        return ""
    try:
        text = extract_text(pdf_path)
        if not text.strip():
            print("No text extracted. The PDF might be empty or text layer inaccessible.")
            return ""
        print(f"Extracted text from {pdf_path} (total length: {len(text)} characters).")
        return text.strip()
    except Exception as e:
        print(f"Failed to extract text with pdfminer: {e}")
        return ""

def clean_text(text):
    """Remove unwanted elements like headers, footers, and extra whitespace."""
    text = re.sub(r'\n\s*\n', '\n', text.strip())
    text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
    return text

def tag_code_snippets(text):
    """Tag Python code snippets with stricter detection."""
    # Stricter regex for Python syntax
    code_pattern = r'^(import\s+|def\s+\w+\s*\(|for\s+\w+\s+in\s+|while\s+\w+|if\s+\w+|class\s+\w+\s*[:\(]|print\s*\()'
    lines = text.split('\n')
    tagged_text = []
    in_code_block = False
    
    for line in lines:
        stripped_line = line.strip()
        if re.match(code_pattern, stripped_line):
            if not in_code_block:
                tagged_text.append("```python")
                in_code_block = True
            tagged_text.append(line)
        elif in_code_block and (not stripped_line or re.match(r'^[A-Za-z\s.,-]+$', stripped_line)):
            tagged_text.append("```")
            in_code_block = False
            tagged_text.append(line)
        else:
            tagged_text.append(line)
    
    if in_code_block:
        tagged_text.append("```")
    return "\n".join(tagged_text)

def preprocess_book():
    """Main function to preprocess the OCR'd book."""
    os.makedirs("data/processed", exist_ok=True)
    if not os.path.exists(OCR_OUTPUT_PATH):
        print(f"OCR'd PDF not found at {OCR_OUTPUT_PATH}. Run OCRmyPDF first:")
        print(f"ocrmypdf --force-ocr {RAW_BOOK_PATH} {OCR_OUTPUT_PATH}")
        return
    
    raw_text = extract_text_from_pdf(OCR_OUTPUT_PATH)
    if not raw_text:
        print("No text extracted. Check the OCR'd PDF.")
        return
    
    cleaned_text = clean_text(raw_text)
    tagged_text = tag_code_snippets(cleaned_text)
    
    with open(PROCESSED_TEXT_PATH, "w", encoding="utf-8") as f:
        f.write(tagged_text)
    print(f"Processed text saved to {PROCESSED_TEXT_PATH}")

if __name__ == "__main__":
    preprocess_book()