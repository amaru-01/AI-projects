import tkinter as tk
from tkinter import messagebox

# Initialize the main application
root = tk.Tk()
root.title("Tic-Tac-Toe Game")

# Initialize variables for game logic
current_player = 'X'
board = [['_' for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]


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


# Function to check if the board is full
def is_board_full():
    for row in board:
        if '_' in row:
            return False
    return True


# Function to handle button clicks (player moves)
def handle_click(row, col):
    global current_player

    if board[row][col] == '_':
        board[row][col] = current_player
        buttons[row][col]['text'] = current_player

        winner = check_winner()

        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            reset_game()
        elif is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()
        else:
            # Switch players
            current_player = 'O' if current_player == 'X' else 'X'
    else:
        messagebox.showwarning("Invalid Move", "This space is already selected.")


# Function to reset the game
def reset_game():
    global board, current_player
    board = [['_' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = '_'


# Create the board buttons
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='_', width=10, height=3,
                                  command=lambda i=i, j=j: handle_click(i, j))
        buttons[i][j].grid(row=i, column=j)

# Start the main application loop
root.mainloop()
