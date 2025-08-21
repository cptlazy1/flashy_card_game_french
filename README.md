# French Flashcard Game

A Python-based flashcard application designed to help users learn French vocabulary through interactive practice sessions.

## Features
- **Interactive Flashcards**: Displays French words with timed reveals of English translations
- **Smart Timer**: 3-second countdown before automatically showing translations
- **Progress Tracking**: Tracks known and unknown words across sessions
- **Persistent Learning**: 
  - Known words are saved to `words_known.csv` and removed from practice
  - Unknown words remain in the practice rotation for continued learning
- **No Duplicate Words**: Prevents showing the same word twice in a row
- **Visual Interface**: Clean Tkinter GUI with custom card images and buttons
- **Data Persistence**: Automatically saves learning progress between sessions
- **Audio Support**: Includes timer sound effects (WAV format)

## Requirements
- Python 3.x
- pandas library
- Tkinter (included with most Python installations)

## Installation
1. Clone this repository
2. Install required dependencies:
   ```bash
   pip install pandas
   ```
3. Ensure you have the required data and image files in their respective folders

## Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. A French word will appear on the front of the card
3. Try to recall the English translation during the 3-second timer
4. The translation will automatically appear on the back of the card
5. Click the checkmark (✓) if you knew the word, or the X if you didn't
6. Known words are permanently removed from practice; unknown words continue in rotation
7. Your progress is automatically saved between sessions

## File Structure
```
flashCardGame/
├── main.py                    # Main application code
├── README.md                  # This file
├── data/
│   ├── french_words.csv       # Original word list
│   ├── words_to_learn.csv     # Current practice words
│   └── words_known.csv        # Words you've mastered
├── images/
│   ├── card_front.png         # Front card design
│   ├── card_back.png          # Back card design
│   ├── right.png              # Check mark button
│   └── wrong.png              # X mark button
└── sounds/
    └── timer_sound.WAV        # Audio feedback
```

## How It Works
- The app starts with words from `french_words.csv`
- As you practice, it creates `words_to_learn.csv` for your current session
- Known words are moved to `words_known.csv` and removed from practice
- Unknown words stay in rotation for continued practice
- Your progress persists between app sessions

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License
