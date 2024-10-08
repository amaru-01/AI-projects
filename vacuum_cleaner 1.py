import tkinter as tk
import random
import time

class VacuumCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacuum Cleaner Simulation")
        
        # Define the grid dimensions
        self.rows = 10
        self.cols = 10
        self.cell_size = 50
        
        # Create canvas to draw the room grid
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()
        
        # Draw the grid cells
        self.cells = {}
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                cell = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgrey", outline="black")
                self.cells[(i, j)] = cell
        
        # Vacuum cleaner's starting position
        self.vacuum_position = [0, 0]
        self.vacuum = self.canvas.create_oval(0, 0, self.cell_size, self.cell_size, fill="blue")
        
        # Randomly "dirty" some cells
        self.dirty_cells = random.sample(list(self.cells.keys()), k=15)
        for cell in self.dirty_cells:
            self.canvas.itemconfig(self.cells[cell], fill="brown")
        
        # Label to display status
        self.status_label = tk.Label(root, text="Automatic vacuum in progress...", font=("Arial", 12))
        self.status_label.pack()
        
        # Start the automatic cleaning process
        self.cleaning_in_progress = True
        self.root.after(1000, self.auto_clean)  # Start after 1 second

    def update_vacuum_position(self):
        # Update the vacuum cleaner's position in the grid
        row, col = self.vacuum_position
        x1, y1 = col * self.cell_size, row * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        self.canvas.coords(self.vacuum, x1, y1, x2, y2)
        
        # Clean the cell if it's dirty
        if tuple(self.vacuum_position) in self.dirty_cells:
            self.dirty_cells.remove(tuple(self.vacuum_position))
            self.canvas.itemconfig(self.cells[tuple(self.vacuum_position)], fill="lightgrey")
        
        # Check if all cells are clean
        if not self.dirty_cells:
            self.status_label.config(text="All cells are clean! Vacuum cleaner job is done.")
            self.cleaning_in_progress = False

    def move_vacuum(self, target_row, target_col):
        """Move the vacuum cleaner step-by-step to the target position."""
        current_row, current_col = self.vacuum_position
        
        if current_row < target_row:
            self.vacuum_position[0] += 1
        elif current_row > target_row:
            self.vacuum_position[0] -= 1
        elif current_col < target_col:
            self.vacuum_position[1] += 1
        elif current_col > target_col:
            self.vacuum_position[1] -= 1
        
        self.update_vacuum_position()

    def find_closest_dirty_cell(self):
        """Find the closest dirty cell to the vacuum's current position."""
        current_row, current_col = self.vacuum_position
        closest_cell = None
        min_distance = float('inf')
        
        for dirty_cell in self.dirty_cells:
            dirty_row, dirty_col = dirty_cell
            distance = abs(current_row - dirty_row) + abs(current_col - dirty_col)
            if distance < min_distance:
                min_distance = distance
                closest_cell = dirty_cell
                
        return closest_cell

    def auto_clean(self):
        """Automatically clean the room by moving towards dirty cells."""
        if self.cleaning_in_progress and self.dirty_cells:
            closest_dirty_cell = self.find_closest_dirty_cell()
            if closest_dirty_cell:
                target_row, target_col = closest_dirty_cell
                self.move_vacuum(target_row, target_col)
            
            # Call this method again to continue cleaning after a short delay
            self.root.after(200, self.auto_clean)
        else:
            self.status_label.config(text="All cells are clean! Vacuum cleaner job is done.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumCleanerApp(root)
    root.mainloop()
