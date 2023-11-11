import unittest
from unittest.mock import patch, MagicMock
from typing import List, Any, Dict, Callable
from io import StringIO

def handle_input(message: str, options: List[str], current_screen: Any, events: Dict[int, Callable[[], None]], invalid_option_message: str) -> None:
    """
    Handles user input by printing a message, displaying a list of options, and executing the corresponding event based on the user's input.

    Parameters:
    - message: The message to be printed.
    - options: A list of options to be displayed.
    - current_screen: The current screen.
    - events: A dictionary mapping option indices to corresponding event functions.
    - invalid_option_message: The message to be displayed when an invalid option is chosen.

    Returns:
    None
    """
    print(message)
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    print(f"{len(options)+1}. Exit")
    event = input()
    if event.isdigit() and 1 <= int(event) <= len(options):
        events[int(event)]()
    elif event == str(len(options)+1):
        exit()
    else:
        print(invalid_option_message)

class TestHandleInput(unittest.TestCase):
    def setUp(self):
        self.message = "Welcome! Please select an option:"
        self.options = ["Option 1", "Option 2", "Option 3"]
        self.current_screen = MagicMock()
        self.events = {
            1: MagicMock(),
            2: MagicMock(),
            3: MagicMock()
        }
        self.invalid_option_message = "Invalid option. Please try again."

    def test_handle_input_valid_option(self):
        with patch("builtins.input", return_value="1"), patch("sys.stdout", new=StringIO()) as fake_output:
            handle_input(self.message, self.options, self.current_screen, self.events, self.invalid_option_message)
            self.events[1].assert_called_once()
            self.assertEqual(fake_output.getvalue(), "Welcome! Please select an option:\n1. Option 1\n2. Option 2\n3. Option 3\n4. Exit\n")

    def test_handle_input_exit_option(self):
        with patch("builtins.input", return_value=str(len(self.options) + 1)), patch("sys.stdout", new=StringIO()) as fake_output, self.assertRaises(SystemExit):
            handle_input(self.message, self.options, self.current_screen, self.events, self.invalid_option_message)
            self.assertEqual(fake_output.getvalue(), "Welcome! Please select an option:\n1. Option 1\n2. Option 2\n3. Option 3\n4. Exit\n")

    def test_handle_input_invalid_option(self):
        with patch("builtins.input", return_value="5"), patch("sys.stdout", new=StringIO()) as fake_output:
            handle_input(self.message, self.options, self.current_screen, self.events, self.invalid_option_message)
            self.assertEqual(fake_output.getvalue(), "Welcome! Please select an option:\n1. Option 1\n2. Option 2\n3. Option 3\n4. Exit\nInvalid option. Please try again.\n")

if __name__ == "__main__":
    unittest.main()