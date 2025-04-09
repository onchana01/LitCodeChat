import re
from src.utils import load_text_file, log_message

# Paths
BOOK_TEXT_PATH = "data/processed/book_text.txt"

def retrieve_section(query, max_context=200):
    """Retrieve a relevant section from the book based on a query."""
    text = load_text_file(BOOK_TEXT_PATH)
    if not text:
        log_message("No book text loaded for retrieval.", "error")
        return "No content available."
    
    # Simple keyword-based retrieval
    query_words = query.lower().split()
    best_match = None
    best_score = 0
    
    for i, line in enumerate(text.split('\n')):
        line_lower = line.lower()
        score = sum(1 for word in query_words if word in line_lower)
        if score > best_score:
            best_score = score
            # Grab context around the line
            start_idx = max(0, i - 5)
            end_idx = min(len(text.split('\n')), i + 6)
            best_match = '\n'.join(text.split('\n')[start_idx:end_idx])
    
    if best_match:
        log_message(f"Retrieved section for query '{query}' with score {best_score}")
        return best_match[:max_context] + "..." if len(best_match) > max_context else best_match
    return "Couldn’t find a relevant section."

if __name__ == "__main__":
    sample_query = "How do I use pandas?"
    result = retrieve_section(sample_query)
    print(result)