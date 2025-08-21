# French Flashcard Game

A simple Python application to help users learn French vocabulary using interactive flashcards.

## Features
- Displays French words and their English translations
- Timer for each card to encourage quick recall
- Mark words as known or unknown
- Words marked as known are removed from practice
- Unknown words are reshuffled for further practice
- Uses CSV for word data and PNG images for card visuals
- Built with Tkinter for a graphical interface

## Installation
1. Clone this repository.
2. Ensure you have Python 3 installed.
3. Install required packages (Tkinter is included with most Python installations).

## Usage
1. Run `main.py`:
   ```bash
   python main.py
   ```
2. The app will display a French word. Try to recall its English meaning.
3. Click the button to reveal the translation.
4. Mark if you know the word (✔️) or not (❌).
5. Known words are removed; unknown words are reshuffled for more practice.

## File Structure
- `main.py`: Main application code
- `data/french_words.csv`: List of French words and their English translations
- `images/`: Contains card and button images

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License

