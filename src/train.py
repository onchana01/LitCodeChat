from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
import torch
from torch.utils.data import Dataset
import os
from src.utils import load_text_file, extract_code_blocks, log_message

# Paths
BOOK_TEXT_PATH = "data/processed/book_text.txt"
FINETUNED_MODEL_PATH = "models/finetuned/litcode_model_gpt2"

class BookCodeDataset(Dataset):
    def __init__(self, text_file, tokenizer, max_length=256):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples = self._prepare_examples(text_file)
    
    def _prepare_examples(self, text_file):
        text = load_text_file(text_file)
        if not text:
            log_message("No text loaded for training.", "error")
            return []
        
        code_blocks = extract_code_blocks(text)
        examples = []
        for code in code_blocks:
            start_idx = text.find(code)
            context_start = max(0, start_idx - 200)
            context = text[context_start:start_idx].strip()
            prompt = f"Question: Generate Python code for a data science task.\nContext: {context}\nCode:\n{code}"
            examples.append(prompt)
        
        log_message(f"Prepared {len(examples)} training examples from {len(code_blocks)} code blocks.")
        return examples
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        encoding = self.tokenizer(
            example,
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        )
        encoding["labels"] = encoding["input_ids"].clone()
        return {key: val.squeeze(0) for key, val in encoding.items()}

def train_model():
    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")  # Smaller model
    tokenizer.pad_token = tokenizer.eos_token
    try:
        model = GPT2LMHeadModel.from_pretrained("distilgpt2", pad_token_id=tokenizer.eos_token_id)
    except Exception as e:
        log_message(f"Failed to load DistilGPT-2 model: {e}", "error")
        return
    
    dataset = BookCodeDataset(BOOK_TEXT_PATH, tokenizer)
    if len(dataset) == 0:
        log_message("No training examples found. Check preprocessing.", "error")
        return
    
    training_args = TrainingArguments(
        output_dir=FINETUNED_MODEL_PATH,
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,  # Accumulate gradients over 4 steps
        save_steps=50,
        save_total_limit=2,
        logging_dir="./logs",
        logging_steps=10,
        learning_rate=5e-5,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )
    
    log_message("Starting training...")
    trainer.train()
    
    model.save_pretrained(FINETUNED_MODEL_PATH)
    tokenizer.save_pretrained(FINETUNED_MODEL_PATH)
    log_message(f"Model fine-tuned and saved to {FINETUNED_MODEL_PATH}")

if __name__ == "__main__":
    os.makedirs(FINETUNED_MODEL_PATH, exist_ok=True)
    train_model()