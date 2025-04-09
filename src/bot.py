from telegram.ext import Application, CommandHandler, MessageHandler, filters
from src.generation import generate_code_solution
from src.utils import log_message
import os
from dotenv import load_dotenv
import random

# Load Telegram token
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Random question templates
QUESTION_TEMPLATES = [
    "How do I create a {topic} array?",
    "How do I plot {topic} data?",
    "How do I filter a {topic} DataFrame?",
    "How do I compute {topic} statistics?",
    "How do I join {topic} datasets?"
]
TOPICS = ["NumPy", "pandas", "matplotlib", "data science"]

async def start(update, context):
    """Handler for /start command."""
    await update.message.reply_text(
        "Welcome to LitCode Chat! I generate Python code solutions from 'Python Data Science Handbook'. "
        "Use /random for a random question or ask me directly (e.g., 'How do I use pandas?')."
    )

async def random_question(update, context):
    """Generate and answer a random question."""
    question = random.choice(QUESTION_TEMPLATES).format(topic=random.choice(TOPICS))
    await update.message.reply_text(f"Random question: {question}")
    response = generate_code_solution(question)
    await update.message.reply_text(response)

async def handle_message(update, context):
    """Handler for user messages."""
    query = update.message.text.strip()
    response = generate_code_solution(query)
    await update.message.reply_text(response)

def main():
    """Run the Telegram bot."""
    if not TELEGRAM_TOKEN:
        log_message("Telegram token not found in .env", "error")
        return
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("random", random_question))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    log_message("Bot started")
    application.run_polling()

if __name__ == "__main__":
    main()