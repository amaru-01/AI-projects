import tkinter as tk
import random

# Agent class
class Agent:
    def __init__(self, env):
        self.x = 1
        self.y = 1
        self.env = env
        self.cleaned_dirt = 0
        self.energy_used = 0
    
    def move(self, direction):
        if direction == "UP" and self.env.is_valid_move(self.x, self.y - 1):
            self.y -= 1
        elif direction == "DOWN" and self.env.is_valid_move(self.x, self.y + 1):
            self.y += 1
        elif direction == "LEFT" and self.env.is_valid_move(self.x - 1, self.y):
            self.x -= 1
        elif direction == "RIGHT" and self.env.is_valid_move(self.x + 1, self.y):
            self.x += 1
        
        self.energy_used += 1
        self.check_for_dirt()

    def check_for_dirt(self):
        if self.env.is_dirt(self.x, self.y):
            self.env.clean_dirt(self.x, self.y)
            self.cleaned_dirt += 1
            self.energy_used += 2  # Extra energy for cleaning

# Environment class
class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.randomize_dirt_and_obstacles()

    def randomize_dirt_and_obstacles(self):
        # Randomly place dirt
        for _ in range(10):  # 10 pieces of dirt
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.grid[y][x] = 1  # 1 represents dirt

        # Randomly place obstacles
        for _ in range(5):  # 5 obstacles
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.grid[y][x] == 0:  # Ensure the obstacle is not placed on dirt
                self.grid[y][x] = 2  # 2 represents an obstacle

    def is_valid_move(self, x, y):
        # Agent cannot move out of bounds or onto an obstacle
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] != 2

    def is_dirt(self, x, y):
        return self.grid[y][x] == 1

    def clean_dirt(self, x, y):
        self.grid[y][x] = 0

# GUI class
class VacuumCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacuum Cleaner Simulator")
        self.env = Environment(10, 10)
        self.agent = Agent(self.env)

        self.is_running = False  # Flag to control simulation

        self.canvas = tk.Canvas(self.root, width=300, height=300)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.delay_label = tk.Label(self.root, text="Time Delay (ms):")
        self.delay_label.grid(row=1, column=0)
        self.delay_entry = tk.Entry(self.root)
        self.delay_entry.grid(row=1, column=1)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_simulation)
        self.start_button.grid(row=1, column=2)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_simulation)  # Stop button
        self.stop_button.grid(row=1, column=3)

        self.randomize_button = tk.Checkbutton(self.root, text="Randomize Dirt & Obstacles", command=self.randomize_dirt)
        self.randomize_button.grid(row=2, column=0, columnspan=2)

        self.stats_label = tk.Label(self.root, text="Dirt Cleaned: 0, Energy Used: 0")
        self.stats_label.grid(row=2, column=2, columnspan=2)

        self.root.bind("<Up>", lambda event: self.move_agent("UP"))
        self.root.bind("<Down>", lambda event: self.move_agent("DOWN"))
        self.root.bind("<Left>", lambda event: self.move_agent("LEFT"))
        self.root.bind("<Right>", lambda event: self.move_agent("RIGHT"))

        self.update_display()

    def randomize_dirt(self):
        self.env.randomize_dirt_and_obstacles()
        self.update_display()

    def start_simulation(self):
        self.is_running = True  # Set flag to True when starting
        delay = int(self.delay_entry.get()) if self.delay_entry.get() else 500
        self.run_step(delay)

    def stop_simulation(self):
        self.is_running = False  # Set flag to False when stopping

    def run_step(self, delay):
        if not self.is_running:
            return  # Exit if the simulation is stopped
        direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.agent.move(direction)
        self.update_display()
        self.root.after(delay, lambda: self.run_step(delay))

    def move_agent(self, direction):
        self.agent.move(direction)
        self.update_display()

    def update_display(self):
        self.canvas.delete("all")
        cell_size = 30
        for y in range(self.env.height):
            for x in range(self.env.width):
                color = "white"
                if self.env.is_dirt(x, y):
                    color = "brown"  # Dirt
                elif self.env.grid[y][x] == 2:
                    color = "black"  # Obstacle
                if self.agent.x == x and self.agent.y == y:
                    color = "red"  # Agent's position
                self.canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill=color)

        # Update stats label
        self.stats_label.config(text=f"Dirt Cleaned: {self.agent.cleaned_dirt}, Energy Used: {self.agent.energy_used}")

# Main
root = tk.Tk()
gui = VacuumCleanerGUI(root)
root.mainloop()
