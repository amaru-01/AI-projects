import tkinter as tk
import random
from tkinter import messagebox

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock, Paper, Scissors Game")

        # Initialize variables
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.total_rounds = 0

        # Create GUI elements
        self.intro_label = tk.Label(root, text="Welcome to Rock, Paper, Scissors!", font=("Arial", 16))
        self.intro_label.pack(pady=10)

        self.round_label = tk.Label(root, text="Enter the number of rounds:", font=("Arial", 14))
        self.round_label.pack(pady=5)

        self.round_entry = tk.Entry(root, font=("Arial", 12))
        self.round_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Game", font=("Arial", 12), command=self.start_game)
        self.start_button.pack(pady=10)

        self.user_choice_label = tk.Label(root, text="Choose Rock, Paper, or Scissors:", font=("Arial", 14))
        self.user_choice_label.pack(pady=10)

        self.rock_button = tk.Button(root, text="Rock", font=("Arial", 12), command=lambda: self.play_round("rock"))
        self.paper_button = tk.Button(root, text="Paper", font=("Arial", 12), command=lambda: self.play_round("paper"))
        self.scissors_button = tk.Button(root, text="Scissors", font=("Arial", 12), command=lambda: self.play_round("scissors"))

        self.rock_button.pack(pady=5)
        self.paper_button.pack(pady=5)
        self.scissors_button.pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(root, text="User: 0 | Computer: 0", font=("Arial", 14))
        self.score_label.pack(pady=5)

        self.end_label = tk.Label(root, text="", font=("Arial", 16))
        self.end_label.pack(pady=10)

    def start_game(self):
        try:
            self.total_rounds = int(self.round_entry.get())
            if self.total_rounds <= 0:
                raise ValueError
            self.rounds_played = 0
            self.user_score = 0
            self.computer_score = 0
            self.score_label.config(text="User: 0 | Computer: 0")
            self.end_label.config(text="")
            self.result_label.config(text="")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of rounds.")

    def play_round(self, user_choice):
        if self.rounds_played >= self.total_rounds:
            self.end_game()
            return

        computer_choice = random.choice(["rock", "paper", "scissors"])
        winner = self.determine_winner(user_choice, computer_choice)
        
        if winner == "user":
            self.user_score += 1
            result_text = f"You chose {user_choice.capitalize()}, Computer chose {computer_choice.capitalize()}. You win this round!"
        elif winner == "computer":
            self.computer_score += 1
            result_text = f"You chose {user_choice.capitalize()}, Computer chose {computer_choice.capitalize()}. Computer wins this round!"
        else:
            result_text = f"You chose {user_choice.capitalize()}, Computer chose {computer_choice.capitalize()}. It's a tie!"

        self.rounds_played += 1
        self.result_label.config(text=result_text)
        self.score_label.config(text=f"User: {self.user_score} | Computer: {self.computer_score}")

        if self.rounds_played == self.total_rounds:
            self.end_game()

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "tie"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            return "user"
        else:
            return "computer"

    def end_game(self):
        if self.user_score > self.computer_score:
            final_result = f"You win the game! Final score: User {self.user_score} - {self.computer_score} Computer."
        elif self.computer_score > self.user_score:
            final_result = f"Computer wins the game! Final score: Computer {self.computer_score} - {self.user_score} User."
        else:
            final_result = f"It's a tie! Final score: User {self.user_score} - {self.computer_score} Computer."
        
        self.end_label.config(text=final_result)
        messagebox.showinfo("Game Over", final_result)

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()
