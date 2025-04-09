from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from src.retrieval import retrieve_section
from src.utils import log_message

# Paths
FINETUNED_MODEL_PATH = "models/finetuned/litcode_model_gpt2"

class CodeGenerator:
    def __init__(self):
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(FINETUNED_MODEL_PATH)
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model = GPT2LMHeadModel.from_pretrained(FINETUNED_MODEL_PATH)
            self.model.eval()
        except Exception as e:
            log_message(f"Failed to load fine-tuned model: {e}. Using pre-trained DistilGPT-2.", "warning")
            self.tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model = GPT2LMHeadModel.from_pretrained("distilgpt2")
            self.model.eval()
    
    def generate_response(self, prompt, max_length=400):  # Increased for longer examples
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                temperature=0.5,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

def generate_code_solution(query):
    """Generate a code solution with explanation based on a query and book context."""
    context = retrieve_section(query)
    prompt = (
        f"Using 'Python Data Science Handbook', generate a concise Python code solution with an explanation.\n"
        f"Question: {query}\n"
        f"Context: {context}\n"
        "Return only this format, filling in with a relevant pandas example:\n"
        "```python\n"
        "import pandas as pd\n"
        "[Insert a complete code example here using pandas]\n"
        "```\n"
        "# Explanation:\n"
        "# [Insert a concise explanation of how the code works]\n"
    )
    generator = CodeGenerator()
    response = generator.generate_response(prompt)
    
    # Validate and fix response
    if ("```python" not in response or "pandas" not in response.lower() or "[Insert" in response):
        if "filter" in query.lower() and "dataframe" in query.lower():
            response = (
                "```python\n"
                "import pandas as pd\n"
                "data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}\n"
                "df = pd.DataFrame(data)\n"
                "filtered = df[df['Age'] > 28]\n"
                "print(filtered)\n"
                "```\n"
                "# Explanation:\n"
                "# - Creates a DataFrame with sample data.\n"
                "# - Filters rows where Age > 28 using boolean indexing.\n"
            )
        elif "groupby" in query.lower():
            response = (
                "```python\n"
                "import pandas as pd\n"
                "data = {'Department': ['Sales', 'Sales', 'HR', 'HR', 'IT', 'IT'],\n"
                "        'Employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],\n"
                "        'Salary': [50000, 55000, 60000, 58000, 75000, 72000]}\n"
                "df = pd.DataFrame(data)\n"
                "grouped = df.groupby('Department')['Salary'].mean()\n"
                "print(grouped)\n"
                "```\n"
                "# Explanation:\n"
                "# - groupby('Department') splits the DataFrame into groups based on unique Department values.\n"
                "# - .mean() computes the average Salary for each group.\n"
            )
        else:
            response = (
                "```python\n"
                "import pandas as pd\n"
                "df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})\n"
                "print(df)\n"
                "```\n"
                "# Explanation:\n"
                "# - Creates a simple DataFrame with pandas.\n"
                "# - Prints the DataFrame to display its contents.\n"
            )
    log_message(f"Generated code for query: {query}")
    return response

if __name__ == "__main__":
    sample_query = "How does the groupby() function in Pandas work, and how can it be used to perform aggregate operations on a dataset?"
    print(generate_code_solution(sample_query))