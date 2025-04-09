import argparse
import os
import yaml
from src.preprocess import preprocess_book
from src.train import train_model
from src.bot import main as run_bot

# Load config with error handling
config_path = "config/config.yaml"
try:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print(f"Config file not found at {config_path}. Using defaults.")
    config = {
        "paths": {
            "raw_book": "data/raw/Python_Datascience.pdf",
            "ocr_output": "data/processed/ocr_output.pdf",
            "processed_text": "data/processed/book_text.txt",
            "finetuned_model": "models/finetuned/litcode_model_gpt2",
            "pretrained_model": "models/pretrained/gpt2"
        },
        "telegram": {"token_env": "TELEGRAM_TOKEN"},
        "training": {"epochs": 3, "batch_size": 4, "max_length": 512}
    }

def run_full_pipeline():
    """Run the full pipeline: preprocess, train, and start bot."""
    print("Starting full pipeline...")
    
    print("Preprocessing Python_Datascience.pdf...")
    preprocess_book()
    
    print("Training the model...")
    train_model()
    
    print("Starting the Telegram bot...")
    run_bot()

def main():
    """Main entry point with command-line arguments."""
    parser = argparse.ArgumentParser(description="LitCode Chat: A Telegram chatbot for Python_Datascience.pdf")
    parser.add_argument("--preprocess", action="store_true", help="Run preprocessing only")
    parser.add_argument("--train", action="store_true", help="Run training only")
    parser.add_argument("--bot", action="store_true", help="Run the bot only")
    parser.add_argument("--full", action="store_true", help="Run the full pipeline (preprocess, train, bot)")
    
    args = parser.parse_args()
    
    if args.preprocess:
        print("Running preprocessing...")
        preprocess_book()
    elif args.train:
        print("Running training...")
        train_model()
    elif args.bot:
        print("Running bot...")
        run_bot()
    elif args.full:
        run_full_pipeline()
    else:
        print("No arguments provided. Use --help for options.")
        parser.print_help()

if __name__ == "__main__":
    # Ensure required directories exist
    for dir_path in ["data/processed", "models/finetuned", "models/pretrained"]:
        os.makedirs(dir_path, exist_ok=True)
    
    main()