import tkinter as tk
from tkinter import messagebox
import random

# Initialize the main application
root = tk.Tk()
root.title("Tic-Tac-Toe: Player vs Computer")

# Initialize game variables
current_player = 'X'  # Player 'X' goes first
board = [['_' for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

# Game stats
user_wins = 0
computer_wins = 0
draws = 0
rounds_left = 0

# Function to check if there's a winner
def check_winner():
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '_':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '_':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '_':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '_':
        return board[0][2]
    return None

# Function to check if the board is full (draw)
def is_board_full():
    for row in board:
        if '_' in row:
            return False
    return True

# Function to handle player's move
def player_move(row, col):
    global current_player

    if board[row][col] == '_':
        board[row][col] = current_player
        buttons[row][col]['text'] = current_player

        winner = check_winner()

        if winner:
            end_game(winner)
        elif is_board_full():
            end_game(None)  # Draw
        else:
            # Switch to computer's turn
            current_player = 'O'
            # Schedule computer's move after a short delay
            root.after(500, computer_move)  # 500 milliseconds (0.5 seconds) delay
    else:
        messagebox.showwarning("Invalid Move", "This space is already selected.")

# Function for computer's move
def computer_move():
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '_']
    if available_moves:
        move = random.choice(available_moves)
        board[move[0]][move[1]] = current_player
        buttons[move[0]][move[1]]['text'] = current_player

        # Display computer's move to the user
        messagebox.showinfo("Computer Move", f"Computer placed 'O' at ({move[0]+1}, {move[1]+1})")

        winner = check_winner()

        if winner:
            end_game(winner)
        elif is_board_full():
            end_game(None)  # Draw
        else:
            # Switch back to player's turn
            current_player = 'X'

# Function to handle the end of a game
def end_game(winner):
    global user_wins, computer_wins, draws, rounds_left

    if winner == 'X':
        user_wins += 1
        messagebox.showinfo("Game Over", "You win!")
    elif winner == 'O':
        computer_wins += 1
        messagebox.showinfo("Game Over", "Computer wins!")
    else:
        draws += 1
        messagebox.showinfo("Game Over", "It's a draw!")

    rounds_left -= 1
    if rounds_left > 0:
        reset_game()
    else:
        show_final_scores()

# Function to show final scores after all rounds are done
def show_final_scores():
    score_message = f"Final Scores:\n\nYou: {user_wins}\nComputer: {computer_wins}\nDraws: {draws}"
    messagebox.showinfo("Final Scores", score_message)
    reset_all()

# Function to reset the game board for a new round
def reset_game():
    global board, current_player
    board = [['_' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = '_'

# Function to reset all variables and start a new set of rounds
def reset_all():
    global user_wins, computer_wins, draws, rounds_left
    user_wins = 0
    computer_wins = 0
    draws = 0
    rounds_left = 0
    prompt_rounds()

# Function to prompt the user for the number of rounds
def prompt_rounds():
    def set_rounds():
        nonlocal round_input
        try:
            rounds = int(round_input.get())
            if rounds <= 0:
                raise ValueError
            global rounds_left
            rounds_left = rounds
            rounds_window.destroy()
            reset_game()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of rounds.")

    rounds_window = tk.Toplevel(root)
    rounds_window.title("Choose Rounds")

    tk.Label(rounds_window, text="Enter number of rounds:").pack(pady=10)
    round_input = tk.Entry(rounds_window)
    round_input.pack(pady=10)
    tk.Button(rounds_window, text="Start", command=set_rounds).pack(pady=10)

# Create the Tic-Tac-Toe board buttons
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='_', width=10, height=3,
                                  command=lambda i=i, j=j: player_move(i, j))
        buttons[i][j].grid(row=i, column=j)

# Start by prompting the user for the number of rounds
prompt_rounds()

# Start the main application loop
root.mainloop()
