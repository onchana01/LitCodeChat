import unittest
from telegram import Update, Message, Chat, User
from telegram.ext import CallbackContext
from src.bot import start, handle_message
from unittest.mock import Mock, patch

class TestBot(unittest.TestCase):
    def setUp(self):
        """Set up mock Telegram objects for testing."""
        self.update = Mock(spec=Update)
        self.context = Mock(spec=CallbackContext)
        
        # Mock message and user
        self.update.message = Mock(spec=Message)
        self.update.message.chat = Mock(spec=Chat)
        self.update.message.from_user = Mock(spec=User)
        self.update.message.chat.id = 12345
        self.update.message.from_user.id = 67890

    def test_start(self):
        """Test the /start command."""
        self.update.message.text = "/start"
        self.update.message.reply_text = Mock()
        
        start(self.update, self.context)
        
        self.update.message.reply_text.assert_called_once()
        call_args = self.update.message.reply_text.call_args[0][0]
        self.assertIn("Welcome to LitCode Chat", call_args)
        self.assertIn("Python_Datascience.pdf", call_args)

    @patch("src.bot.get_relevant_section")
    @patch("src.bot.generate_code_or_explanation")
    def test_handle_message(self, mock_generate, mock_retrieve):
        """Test handling a user message."""
        # Mock retrieval and generation responses
        mock_retrieve.return_value = "From the book: ```python\nimport pandas as pd\n```"
        mock_generate.return_value = "```python\ndf = pd.DataFrame({'A': [1, 2]})\n```"
        
        self.update.message.text = "How do I use pandas?"
        self.update.message.reply_text = Mock()
        
        handle_message(self.update, self.context)
        
        self.update.message.reply_text.assert_called_once()
        response = self.update.message.reply_text.call_args[0][0]
        self.assertIn("From the book", response)
        self.assertIn("import pandas as pd", response)
        self.assertIn("df = pd.DataFrame", response)
        self.assertIn("Here’s more", response)

    @patch("src.bot.get_relevant_section")
    @patch("src.bot.generate_code_or_explanation")
    def test_handle_message_long_response(self, mock_generate, mock_retrieve):
        """Test handling a long message that exceeds Telegram's 4096 char limit."""
        # Create a long mock response
        long_text = "Long text " * 500  # ~5000 chars
        mock_retrieve.return_value = "From the book: Short text"
        mock_generate.return_value = long_text
        
        self.update.message.text = "Explain something long"
        self.update.message.reply_text = Mock()
        
        handle_message(self.update, self.context)
        
        # Check that reply_text was called multiple times due to splitting
        self.assertTrue(self.update.message.reply_text.call_count > 1)
        first_chunk = self.update.message.reply_text.call_args_list[0][0][0]
        self.assertIn("From the book", first_chunk)
        self.assertTrue(len(first_chunk) <= 4096)

if __name__ == "__main__":
    unittest.main()