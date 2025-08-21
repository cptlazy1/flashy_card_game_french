# --- Imports ---
from tkinter import *
import pandas as pd
import random

# --- Constants / Config ---
BACKGROUND_COLOR = "#B1DDC6"
COUNTDOWN_SECONDS = 3  # Seconds to wait before revealing translation

# --- State Variables ---
current_word = {}
timer = None          # after() id for the scheduled translation reveal
timer_count = 0       # remaining seconds in visible countdown

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
word_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
translation_text = canvas.create_text(400, 263, text="", font=("Ariel", 40, "bold"))
timer_text = canvas.create_text(750, 50, text="", font=("Ariel", 24, "bold"), fill="red")
check_img = PhotoImage(file="images/right.png")
cross_img = PhotoImage(file="images/wrong.png")
check_button = Button(image=check_img, highlightthickness=0)
check_button.grid(row=1, column=1)
cross_button = Button(image=cross_img, highlightthickness=0)
cross_button.grid(row=1, column=0)

# --- Data Loading ---
# We keep a working list 'data' of dicts, each dict like: {"French": "...", "English": "..."}.
# 1. First try to load the user's progress file (words still to learn).
# 2. If it does not exist (first run), fall back to the full source list.
# 3. Convert the resulting DataFrame into a list[dict] for quick random.choice usage.
# NOTE: Ensure CSV files have columns exactly: French,English
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    data = original_data.to_dict(orient="records")
else:
    data = data.to_dict(orient="records")

# --- Functions ---
def show_word():
    """Show a new French word, start (and display) the countdown, disable buttons."""
    global current_word, timer, timer_count
    # Cancel any pending translation reveal to avoid race conditions if user advances quickly.
    if timer is not None:
        window.after_cancel(timer)
    check_button.config(state=DISABLED)
    cross_button.config(state=DISABLED)
    current_word = random.choice(data)
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(word_text, text=current_word["French"])
    canvas.itemconfig(translation_text, text="")
    timer_count = COUNTDOWN_SECONDS
    update_timer()
    timer = window.after(COUNTDOWN_SECONDS * 1000, show_translation)

def update_timer():
    """Update the visible numeric countdown."""
    global timer_count
    if timer_count > 0:
        canvas.itemconfig(timer_text, text=str(timer_count))
        timer_count -= 1
        window.after(1000, update_timer)
    else:
        canvas.itemconfig(timer_text, text="")

def show_translation():
    """Reveal the English translation and re-enable interaction buttons."""
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(translation_text, text=current_word["English"])
    canvas.itemconfig(timer_text, text="")
    check_button.config(state=NORMAL)
    cross_button.config(state=NORMAL)

def on_check():
    """User knows the word: remove it from practice list and show next."""
    data.remove(current_word)
    show_word()

def on_cross():
    """User does not know the word: keep it (simple reshuffle logic) and show next."""
    # Move current word toward the end (light-weight spacing before it reappears).
    for i, word in enumerate(data):
        if word == current_word:
            data.append(data.pop(i))
            break
    show_word()

check_button.config(command=on_check)
cross_button.config(command=on_cross)

show_word()
window.mainloop()
