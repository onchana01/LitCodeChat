# LitCode Chat

A Telegram chatbot that generates Python code solutions based on the *"Python Data Science Handbook"* by Jake VanderPlas. Ask it data science questions, get concise code examples with explanations, or request a random question from the book!

Built with DistilGPT-2 fine-tuned on code snippets from the book, it preprocesses text, trains a model, retrieves relevant context, and generates responses—all integrated into a Telegram bot.

## Features
- **Code Generation**: Answers questions like "How does `groupby()` work in Pandas?" with code and explanations.
- **Random Questions**: Use `/random` to get a question from the book with a solution.
- **Fallback Mechanism**: Ensures quality responses when the model struggles.
- **Telegram Integration**: Chat with `@LitCodeChatBot` (replace with your bot’s handle).

## Prerequisites
- Python 3.8+
- Telegram account and bot token from [BotFather](https://t.me/BotFather)
- Dependencies: `transformers`, `torch`, `python-telegram-bot`, `PyYAML`, `pandas`

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/onchana01/LitCodeChat.git
   cd LitCodeChat

Create Virtual Environment:
bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Install Dependencies:
bash

pip install -r requirements.txt

(Note: Add a requirements.txt with pip freeze > requirements.txt after installing packages.)

Set Up Telegram Token:
Create a .env file:

TELEGRAM_TOKEN=your_bot_token_here

Prepare the Book:
Place PythonDataScienceHandbook.pdf in data/raw/ (or adjust config.yaml).

Usage
Preprocess the Book:
bash

python main.py --preprocess

Outputs code blocks to data/processed/book_text.txt.

Train the Model:
bash

python main.py --train

Fine-tunes DistilGPT-2, saves to models/finetuned/.

Run the Bot:
bash

python main.py --bot

Starts polling Telegram for messages.

Interact on Telegram:
/start: Welcome message.

/random: Random question and solution.

Ask directly: e.g., "How do I filter a DataFrame?"

Example Interaction

> /start
Welcome to LitCode Chat! I generate Python code solutions from 'Python Data Science Handbook'. Use /random or ask me directly (e.g., 'How do I use pandas?').

> How does groupby() work in Pandas?
```python
import pandas as pd
data = {'Department': ['Sales', 'Sales', 'HR'], 'Salary': [50000, 55000, 60000]}
df = pd.DataFrame(data)
grouped = df.groupby('Department')['Salary'].mean()
print(grouped)

Explanation:
- groupby('Department') splits the DataFrame by unique Department values.
- .mean() computes the average Salary per group.

Future Improvements
- Enhance model training with more epochs or a larger dataset.
- Add support for NumPy, Matplotlib, and other book topics.
- Improve retrieval with embeddings for better context.

License
MIT License (feel free to adjust).

Acknowledgments
- *"Python Data Science Handbook"* by Jake VanderPlas.
- Built with ❤️ by [onchana01](https://github.com/onchana01).

