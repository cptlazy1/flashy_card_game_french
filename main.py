# --- Imports ---
from tkinter import *
import pandas as pd
import random
import pygame

# --- Constants / Config ---
BACKGROUND_COLOR = "#B1DDC6"
COUNTDOWN_SECONDS = 3
FRONT_TEXT_COLOR = "#000000"
BACKGROUND_TEXT_COLOR = "#FFFFFF"

# --- Initialize Sound ---
pygame.mixer.init()
try:
    timer_sound = pygame.mixer.Sound("sounds/timer_sound.wav")
except pygame.error:
    timer_sound = None  # Graceful fallback if sound file missing

# --- State Variables ---
current_word = {}     # Currently displayed word dictionary
previous_word = None  # Prevent consecutive duplicate words
timer = None          # Timer ID for auto-revealing translation
timer_count = 0       # Countdown display value
data = []            # Active practice list (words still to learn)

# --- UI Setup ---
window = Tk()
window.title("Flashy")
window.minsize(880, 700)
window.maxsize(880, 700)
window.config(padx=50, pady=40, bg=BACKGROUND_COLOR)

sound_enabled = BooleanVar(value=True)  # Sound toggle state

# Canvas and card images
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=4)

# Text elements on canvas
word_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill=FRONT_TEXT_COLOR)
translation_text = canvas.create_text(400, 263, text="", font=("Ariel", 40, "bold"), fill=BACKGROUND_TEXT_COLOR)
timer_text = canvas.create_text(750, 50, text="", font=("Ariel", 24, "bold"), fill="red")

# Button images and controls
check_img = PhotoImage(file="images/right.png")
cross_img = PhotoImage(file="images/wrong.png")

# Button layout: Cross | Quit | Sound Toggle | Check
cross_button = Button(image=cross_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0, relief="flat")
cross_button.grid(row=1, column=0)

quit_button = Button(text="Quit", font=("Arial", 12, "bold"), bg="red", fg="white",
                    highlightthickness=0, borderwidth=0, relief="flat", padx=20, pady=5)
quit_button.grid(row=1, column=1, padx=10)

sound_toggle = Checkbutton(text="Sound", variable=sound_enabled, font=("Arial", 10),
                          bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0)
sound_toggle.grid(row=1, column=2, padx=10)

check_button = Button(image=check_img, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0, relief="flat")
check_button.grid(row=1, column=3)

# --- Data Loading ---
# Persistence: Load existing progress or initialize from original word list
try:
    data_df = pd.read_csv("data/words_to_learn.csv")
    data = data_df.to_dict(orient="records")
except FileNotFoundError:
    # First run: copy original list to create initial practice list
    original_data = pd.read_csv("data/french_words.csv")
    data = original_data.to_dict(orient="records")
    pd.DataFrame(data).to_csv("data/words_to_learn.csv", index=False)

# --- Core Game Functions ---
def show_word():
    """Display new French word and start 3-second countdown before revealing translation."""
    global current_word, previous_word, timer, timer_count

    # Check for game completion
    if not data:
        show_congratulations()
        return

    # Clean up any existing timer
    if timer is not None:
        window.after_cancel(timer)
        timer = None

    # Select random word, avoiding immediate repeats
    if len(data) > 1:
        current_word = random.choice(data)
        while current_word == previous_word:
            current_word = random.choice(data)
    else:
        current_word = random.choice(data)

    previous_word = current_word

    # Disable user interaction during countdown
    check_button.config(state="disabled")
    cross_button.config(state="disabled")

    # Display French word on front of card
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(word_text, text=current_word["French"])
    canvas.itemconfig(translation_text, text="")

    # Start countdown timer
    timer_count = COUNTDOWN_SECONDS
    update_timer()
    timer = window.after(COUNTDOWN_SECONDS * 1000, show_translation)

def update_timer():
    """Update countdown display and play tick sound each second."""
    global timer_count
    if timer_count > 0:
        canvas.itemconfig(timer_text, text=str(timer_count))
        # Play tick sound if enabled and available
        if timer_sound and sound_enabled.get():
            timer_sound.play()
        timer_count -= 1
        window.after(1000, update_timer)
    else:
        canvas.itemconfig(timer_text, text="")

def show_translation():
    """Reveal English translation on back of card and enable user interaction."""
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(translation_text, text=current_word["English"])
    canvas.itemconfig(timer_text, text="")
    check_button.config(state="normal")
    cross_button.config(state="normal")

# --- Game Completion & Reset ---
def show_congratulations():
    """Display completion message and auto-restart game."""
    global data

    if timer is not None:
        window.after_cancel(timer)

    # Display completion message
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(word_text, text="Congratulations!")
    canvas.itemconfig(translation_text, text="You've learned all words!\nRestarting...")
    canvas.itemconfig(timer_text, text="")
    check_button.config(state="disabled")
    cross_button.config(state="disabled")

    # Auto-restart after 3 seconds
    window.after(3000, reset_game)

def reset_game():
    """Reload original word list and restart game cycle."""
    global data

    # Reset to full word list
    original_data = pd.read_csv("data/french_words.csv")
    data = original_data.to_dict(orient="records")

    # Update practice list file
    pd.DataFrame(data).to_csv("data/words_to_learn.csv", index=False)

    show_word()

# --- User Actions ---
def on_check():
    """Handle 'known word': move to learned list and continue."""
    global data

    # Track learned words
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
        pd.DataFrame(columns=["French", "English"]).to_csv("data/words_to_learn.csv", index=False)

    show_word()

def on_cross():
    """Handle 'unknown word': keep in practice rotation."""
    # Move word to end for later review
    data.remove(current_word)
    data.append(current_word)
    show_word()

def quit_game():
    """Exit application."""
    window.destroy()

# --- Event Binding ---
check_button.config(command=on_check)
cross_button.config(command=on_cross)
quit_button.config(command=quit_game)

# --- Start Game ---
show_word()
window.mainloop()
