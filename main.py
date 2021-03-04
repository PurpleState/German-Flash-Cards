from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE = "German"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/german_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}
words_to_learn = {}


# ---------------------------- CREATE NEW FLASH CARDS ------------------------------- #


def next_card():
    # check if words to learn is populated
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text=LANGUAGE, fill="black")
    canvas.itemconfig(card_word, text=current_card[LANGUAGE], fill="black")
    canvas.itemconfig(background, image=front_img)
    flip_timer = window.after(3000, func=flip_card)

# ---------------------------- CREATE NEW FLASH CARDS ------------------------------- #


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(background, image=back_img)


# ---------------------------- UPDATING FLASH CARDS ------------------------------- #
def update_deck():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = PhotoImage(file='images/card_front.png')
back_img = PhotoImage(file='images/card_back.png')
background = canvas.create_image(400, 263, image=front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_img = PhotoImage(file='images/right.png')
right_button = Button(image=right_img, highlightthickness=0, command=update_deck)
right_button.grid(column=0, row=1)

wrong_img = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()

window.mainloop()
