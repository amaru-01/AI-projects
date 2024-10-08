import random

# Define the environment grid
class VacuumCleanerEnv:
    def __init__(self, rows, cols, dirt_percentage=0.2):
        self.rows = rows
        self.cols = cols
        # Create a grid with dirt randomly distributed
        self.grid = [['.' for _ in range(cols)] for _ in range(rows)]  # '.' means clean
        self.dirt_percentage = dirt_percentage
        self.place_dirt()
        self.place_obstacles()
        self.agent_pos = [0, 0]  # Initial position of the vacuum cleaner
    
    def place_dirt(self): #called to randomly distribute dirt ('D') over the grid
        total_cells = self.rows * self.cols
        num_dirt_cells = int(self.dirt_percentage * total_cells)
        dirt_positions = random.sample(range(total_cells), num_dirt_cells)
        for pos in dirt_positions:
            row, col = divmod(pos, self.cols)
            self.grid[row][col] = 'D'  # 'D' means dirt
    
    def place_obstacles(self): #called to randomly place obstacles ('O') in the grid
        total_cells = self.rows * self.cols
        num_obstacles = random.randint(1, int(total_cells * 0.1))  # 10% of grid max
        obstacle_positions = random.sample(range(total_cells), num_obstacles)
        for pos in obstacle_positions:
            row, col = divmod(pos, self.cols)
            self.grid[row][col] = 'O'  # 'O' means obstacle

    def display(self):
        for row in self.grid:
            print(" ".join(row))
        print(f"Agent position: {self.agent_pos}")
    
    def is_dirty(self, pos): #checks whether the current cell is dirty ('D')
        row, col = pos
        return self.grid[row][col] == 'D'

    def clean(self, pos): #cleans the current cell, changing it from dirty ('D') to clean ('.')
        row, col = pos
        if self.grid[row][col] == 'D':
            self.grid[row][col] = '.'
            print(f"Cleaned dirt at {pos}")

    def is_obstacle(self, pos): #checks if a given position contains an obstacle ('O').
        row, col = pos
        return self.grid[row][col] == 'O'
    
    def move_agent(self, direction): #method is responsible for moving the vacuum cleaner in one of four directions
        row, col = self.agent_pos
        if direction == 'up' and row > 0:
            new_pos = [row - 1, col]
        elif direction == 'down' and row < self.rows - 1:
            new_pos = [row + 1, col]
        elif direction == 'left' and col > 0:
            new_pos = [row, col - 1]
        elif direction == 'right' and col < self.cols - 1:
            new_pos = [row, col + 1]
        else:
            print("Movement blocked (edge of grid or obstacle)")
            return False

        if self.is_obstacle(new_pos):
            print("Movement blocked by obstacle")
            return False
        self.agent_pos = new_pos
        return True

# Define the Vacuum Cleaner agent
class VacuumCleanerAgent:
    def __init__(self, env):
        self.env = env
    
    def random_move(self):
        directions = ['up', 'down', 'left', 'right'] #The possible movement directions.
        while True:
            direction = random.choice(directions) #Picks a random direction for the agent to try moving.
            if self.env.move_agent(direction):
                break
    
    def clean(self):
        if self.env.is_dirty(self.env.agent_pos): #agent checks if the current are is dirty
            self.env.clean(self.env.agent_pos) #if dirty, clean it
    
    def run(self, steps=20): #number of steps the vaccum cleaner will run
        for step in range(steps):
            print(f"Step {step + 1}")
            self.clean()  # Clean if the current position is dirty
            self.random_move()  # Move randomly
            self.env.display()

# Initialize environment and agent
env = VacuumCleanerEnv(5, 5) #number of grids in the 2D martix
agent = VacuumCleanerAgent(env) #calling the class of env

# Run the vacuum cleaner agent for 20 steps
agent.run(steps=20)
