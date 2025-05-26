import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import random
import os

# --- Load words from CSV ---
def load_words(filename):
    words = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            words.append((row[0].strip(), row[1].strip()))
    return words

# --- Paths ---
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "words.csv")
word_list = load_words(csv_path)

# --- Game State ---
player_hp = 100
monster_hp = 100
score = 0
difficulty = None
num_choices = 3  # Default difficulty

# --- App Setup ---
root = tk.Tk()
root.title("Word Warrior")

question_label = tk.Label(root, text="Press Start to Begin", font=("Helvetica", 14))
question_label.pack(pady=20)

style = ttk.Style()
style.theme_use('clam')  # Use a theme that supports bar styling
style.configure("green.Horizontal.TProgressbar", throughcolor='white', background='green', thickness=20)


buttons = []
for i in range(4):  # Max 4 options for Hard
    btn = tk.Button(root, text="", width=50, font=("Helvetica", 12), state="disabled")
    btn.pack(pady=5)
    buttons.append(btn)

status_label = tk.Label(root, text="HP: You 100 | Monster 100", font=("Helvetica", 12))
status_label.pack(pady=10)

monster_health_bar = ttk.Progressbar(root, orient='horizontal', length=250, mode='determinate', style="green.Horizontal.TProgressbar", maximum=100)
monster_health_bar.pack(pady=10)
monster_health_bar['value'] = 100


score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 12))
score_label.pack(pady=5)

# --- Start Game ---
def set_difficulty(level):
    global difficulty, num_choices
    difficulty = level
    if level == "Easy":
        num_choices = 2
    elif level == "Medium":
        num_choices = 3
    else:
        num_choices = 4

    # Hide difficulty buttons
    for btn in difficulty_buttons:
        btn.pack_forget()

    # Show start button
    start_btn.pack(pady=20)
    question_label.config(text=f"Difficulty set to {difficulty}. Click Start to begin!")

# --- Start Game ---
def start_game():
    global player_hp, monster_hp, score
    player_hp = 100
    monster_hp = 100
    score = 0
    score_label.config(text="Score: 0")
    status_label.config(text="HP: You 100 | Monster 100")
    start_btn.pack_forget()
    next_question()


# --- Show Next Question ---
def next_question():
    global correct_def
    word, correct_def = random.choice(word_list)
    wrong_defs = [w[1] for w in random.sample(word_list, 10) if w[1] != correct_def]
    choices = wrong_defs[:num_choices - 1] + [correct_def]
    random.shuffle(choices)

    question_label.config(text=f"What is the definition of: {word}")
    for i in range(len(buttons)):
        if i < num_choices:
            buttons[i].config(text=choices[i], command=lambda c=choices[i]: check_answer(c), state="normal")
        else:
            buttons[i].config(text="", state="disabled")

# --- Check Answer ---
def check_answer(selected):
    global player_hp, monster_hp, score

    correct = (selected == correct_def)
    damage = random.randint(10, 20)

    # Update stats based on correctness
    if correct:
        monster_hp -= damage
        monster_health_bar['value'] = max(monster_hp, 0)  # Prevents it from going below 0
        animate_bar(monster_health_bar, monster_health_bar['value'], max(monster_hp, 0))
        monster_health_bar['value'] = monster_hp
        fix_bar_color(monster_health_bar)
        score += 1
        status_label.config(text=f"✅ Correct! You hit the monster for {damage} damage.")
    else:
        player_hp -= damage
        status_label.config(text=f"❌ Wrong! The monster hit you for {damage} damage.")

    # Update score display
    score_label.config(text=f"Score: {score}")

    # --- BUTTON FEEDBACK LOGIC ---
    for btn in buttons:
        btn.config(state="disabled")  # Disable all
        if btn['text'] == selected:
            btn.config(bg="green" if correct else "red")  # Feedback color

    # Check for game over after delay
    root.after(1000, lambda: handle_after_answer())


def handle_after_answer():
    # Reset button colors
    for btn in buttons:
        btn.config(bg="SystemButtonFace")  # Reset to default

    # Check if game is over
    if monster_hp <= 0:
        messagebox.showinfo("Victory", f"You won! 🎉\nFinal score: {score}\nYour HP: {player_hp}")
        for btn in buttons:
            btn.config(state="disabled")
    elif player_hp <= 0:
        messagebox.showinfo("Defeat", f"You lost! 💀\nFinal score: {score}")
        for btn in buttons:
            btn.config(state="disabled")
    else:
        next_question()
    monster_health_bar['value'] = 0


def animate_bar(bar, start, end, step=-1):
    if start <= end:
        bar['value'] = end
        return
    bar['value'] = start
    bar.config(style='green.Horizontal.TProgressbar')
    root.after(10, lambda: animate_bar(bar, start + step, end, step))

def fix_bar_color(bar):
    bar.config(style="green.Horizontal.TProgressbar")
    bar.update_idletasks()






# --- Start Button ---
question_label.config(text="Choose Difficulty to Begin")

difficulty_buttons = []

for level in ["Easy", "Medium", "Hard"]:
    b = tk.Button(root, text=level, width=20, font=("Helvetica", 12),
                  command=lambda l=level: set_difficulty(l))
    b.pack(pady=5)
    difficulty_buttons.append(b)

start_btn = tk.Button(root, text="Start Game", command=start_game, font=("Helvetica", 12))
start_btn.pack(pady=20)

# --- Main Loop ---
root.mainloop()
