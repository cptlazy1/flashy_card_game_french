# --- Imports ---
from tkinter import *
import pandas as pd
import random
import pygame

# --- Constants / Config ---
BACKGROUND_COLOR = "#B1DDC6"
COUNTDOWN_SECONDS = 3  # Seconds to wait before revealing translation
FRONT_TEXT_COLOR = "#000000"
BACKGROUND_TEXT_COLOR = "#FFFFFF"

# --- Initialize Sound ---
pygame.mixer.init()
try:
    timer_sound = pygame.mixer.Sound("sounds/timer_sound.wav")
except pygame.error:
    timer_sound = None  # Fallback if sound file not found

# --- State Variables ---
current_word = {}
previous_word = None  # Track the last shown word to avoid duplicates
timer = None          # after() id for the scheduled translation reveal
timer_count = 0       # remaining seconds in visible countdown
data = []            # Practice list - words still to learn

# --- UI Setup ---
window = Tk()
window.title("Flashy")
window.minsize(880, 700)
window.maxsize(880, 700)
window.config(padx=50, pady=40, bg=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)
word_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill=FRONT_TEXT_COLOR)
translation_text = canvas.create_text(400, 263, text="", font=("Ariel", 40, "bold"), fill=BACKGROUND_TEXT_COLOR)
timer_text = canvas.create_text(750, 50, text="", font=("Ariel", 24, "bold"), fill="red")
check_img = PhotoImage(file="images/right.png")
cross_img = PhotoImage(file="images/wrong.png")
check_button = Button(image=check_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0, relief="flat")
check_button.grid(row=1, column=1)
cross_button = Button(image=cross_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0, relief="flat")
cross_button.grid(row=1, column=0)

# --- Data Loading ---
# Load practice list if it exists, otherwise create from original list
try:
    data_df = pd.read_csv("data/words_to_learn.csv")
    data = data_df.to_dict(orient="records")
except FileNotFoundError:
    # First time: copy original list to practice list
    original_data = pd.read_csv("data/french_words.csv")
    data = original_data.to_dict(orient="records")
    pd.DataFrame(data).to_csv("data/words_to_learn.csv", index=False)

# --- Functions ---
def show_word():
    """Show a new French word, start countdown, disable buttons."""
    global current_word, previous_word, timer, timer_count

    # Check if practice list is empty
    if not data:
        show_congratulations()
        return

    # Cancel any pending translation reveal
    if timer is not None:
        window.after_cancel(timer)
        timer = None

    # Prevent showing the same word twice in a row
    if len(data) > 1:
        current_word = random.choice(data)
        while current_word == previous_word:
            current_word = random.choice(data)
    else:
        current_word = random.choice(data)

    previous_word = current_word

    check_button.config(state="disabled")
    cross_button.config(state="disabled")
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(word_text, text=current_word["French"])
    canvas.itemconfig(translation_text, text="")
    timer_count = COUNTDOWN_SECONDS
    update_timer()
    timer = window.after(COUNTDOWN_SECONDS * 1000, show_translation)


def update_timer():
    """Update the visible numeric countdown and play timer sound."""
    global timer_count
    if timer_count > 0:
        canvas.itemconfig(timer_text, text=str(timer_count))
        # Play timer sound if available
        if timer_sound:
            timer_sound.play()
        timer_count -= 1
        window.after(1000, update_timer)
    else:
        canvas.itemconfig(timer_text, text="")

def show_translation():
    """Reveal the English translation and re-enable interaction buttons."""
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(translation_text, text=current_word["English"])
    canvas.itemconfig(timer_text, text="")
    check_button.config(state="normal")
    cross_button.config(state="normal")

def show_congratulations():
    """Show congratulatory message and reset the game."""
    global data

    # Cancel any pending timer
    if timer is not None:
        window.after_cancel(timer)

    # Show congratulations
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(word_text, text="Congratulations!")
    canvas.itemconfig(translation_text, text="You've learned all words!\nRestarting...")
    canvas.itemconfig(timer_text, text="")
    check_button.config(state="disabled")
    cross_button.config(state="disabled")

    # Reset game after 3 seconds
    window.after(3000, reset_game)

def reset_game():
    """Reset the game by reloading the original word list."""
    global data

    # Reload original list
    original_data = pd.read_csv("data/french_words.csv")
    data = original_data.to_dict(orient="records")

    # Save reset practice list
    pd.DataFrame(data).to_csv("data/words_to_learn.csv", index=False)

    # Start new game
    show_word()

def on_check():
    """User knows the word: move to known list and show next."""
    global data

    # Add to known words list
    try:
        known_words = pd.read_csv("data/words_known.csv")
    except FileNotFoundError:
        known_words = pd.DataFrame(columns=["French", "English"])

    # Add current word to known words
    new_known = pd.DataFrame([current_word])
    known_words = pd.concat([known_words, new_known], ignore_index=True)
    known_words.to_csv("data/words_known.csv", index=False)

    # Remove from practice list
    data.remove(current_word)

    # Update practice list file
    if data:
        pd.DataFrame(data).to_csv("data/words_to_learn.csv", index=False)
    else:
        # Create empty file if no words left
        pd.DataFrame(columns=["French", "English"]).to_csv("data/words_to_learn.csv", index=False)

    show_word()

def on_cross():
    """User does not know the word: keep in practice list and show next."""
    # Move word to end of list for later practice
    data.remove(current_word)
    data.append(current_word)
    show_word()

# --- Main ---
check_button.config(command=on_check)
cross_button.config(command=on_cross)

show_word()

window.mainloop()
