import os
import csv
import random

# Load words from CSV
def load_words(filename):
    words = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            words.append((row[0].strip(), row[1].strip()))
    return words

# Game variables
player_hp = 100
monster_hp = 100
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "words.csv")
word_list = load_words(csv_path)


print("🔥 Welcome to Word Warrior 🔥")
print("Defeat the Word Monster by answering correctly!")
print('--------------------------------------------------------------------')

# Ask for difficulty level
print("\nChoose difficulty:")
print("1. Easy (2 choices)")
print("2. Medium (3 choices)")
print("3. Hard (4 choices)")

difficulty = input("Enter difficulty level (1-3): ")
if difficulty == '1':
    num_choices = 2
    monster_hit_range = (5, 10)
    player_hit_range = (15, 25)
elif difficulty == '3':
    num_choices = 4
    monster_hit_range = (15, 25)
    player_hit_range = (5, 10)
else:
    num_choices = 3
    monster_hit_range = (10, 20)
    player_hit_range = (10, 20)


# Game loop
score = 0
while player_hp > 0 and monster_hp > 0:
    word, correct_def = random.choice(word_list)
    
    # Create wrong choices
    wrong_defs = [w[1] for w in random.sample(word_list, num_choices + 2) if w[1] != correct_def]
    choices = wrong_defs[:num_choices - 1] + [correct_def]
    random.shuffle(choices)

    print(f"\n⚔️ What is the meaning of: **{word}**")
    for i, option in enumerate(choices):
        print(f"  {i+1}. {option}")
    
    try:
        answer = int(input(f"Your choice (1-{num_choices}): "))
        if choices[answer - 1] == correct_def:
            damage = random.randint(*player_hit_range)
            monster_hp -= damage
            score += 1
            print(f"✅ Correct! You hit the monster for {damage} damage.")
        else:
            damage = random.randint(*monster_hit_range)
            player_hp -= damage
            print(f"❌ Wrong! The monster hit you for {damage} damage.")
    except (ValueError, IndexError):
        print("⚠️ Invalid input! Monster strikes while you're confused.")
        player_hp -= 10
    
    print(f"❤️ Your HP: {player_hp} | 👾 Monster HP: {monster_hp}")

# End game
if player_hp <= 0:
    print("\n💀 You were defeated... Try again!")
else:
    print("\n🏆 Victory! The Word Monster has been defeated!")
print(f"\n📊 Final Score: {score} correct answers!")

