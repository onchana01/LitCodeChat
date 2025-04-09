import re
import logging
import os

# Set up logging
logging.basicConfig(
    filename="litcodechat.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_message(message, level="info"):
    """Log a message to the log file."""
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)
    elif level == "warning":
        logging.warning(message)

def load_text_file(file_path):
    """Load text from a file with error handling."""
    if not os.path.exists(file_path):
        log_message(f"File not found: {file_path}", "error")
        return ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        log_message(f"Loaded text from {file_path} (length: {len(text)} characters)")
        return text
    except Exception as e:
        log_message(f"Error loading file {file_path}: {e}", "error")
        return ""

def save_text_file(file_path, text):
    """Save text to a file with error handling."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        log_message(f"Saved text to {file_path} (length: {len(text)} characters)")
        return True
    except Exception as e:
        log_message(f"Error saving file {file_path}: {e}", "error")
        return False

def extract_code_blocks(text):
    """Extract all Python code blocks from text."""
    code_pattern = r'```python\n(.*?)\n```'
    code_blocks = re.findall(code_pattern, text, re.DOTALL)
    return code_blocks

def truncate_text(text, max_length=512):
    """Truncate text to a maximum length, preserving whole words."""
    if len(text) <= max_length:
        return text
    truncated = text[:max_length].rsplit(" ", 1)[0]
    log_message(f"Truncated text from {len(text)} to {len(truncated)} characters", "warning")
    return truncated

if __name__ == "__main__":
    # Test the utils
    sample_text = load_text_file("data/processed/book_text.txt")
    if sample_text:
        code_blocks = extract_code_blocks(sample_text)
        print(f"Found {len(code_blocks)} code blocks. First one:\n{code_blocks[0] if code_blocks else 'None'}")
        truncated = truncate_text(sample_text, 100)
        print(f"Truncated text:\n{truncated}")