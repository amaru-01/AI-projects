import tkinter as tk
from tkinter import ttk, messagebox
import time
from queue import PriorityQueue

# Define the Romanian map with distances (weighted graph)
romania_map = {
    'Arad': {'Sibiu': 140, 'Timisoara': 118, 'Zerind': 75},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

# Define positions for each city for visualization purposes
city_positions = {
    'Arad': (50, 300), 'Zerind': (70, 200), 'Oradea': (90, 120), 'Timisoara': (100, 400),
    'Lugoj': (150, 500), 'Mehadia': (200, 600), 'Drobeta': (250, 700), 'Craiova': (350, 650),
    'Sibiu': (150, 200), 'Rimnicu Vilcea': (250, 300), 'Fagaras': (300, 200), 'Pitesti': (400, 400),
    'Bucharest': (500, 300), 'Giurgiu': (550, 400), 'Urziceni': (550, 200), 'Hirsova': (650, 150),
    'Eforie': (700, 100), 'Vaslui': (650, 250), 'Iasi': (600, 300), 'Neamt': (550, 350)
}

# Create the Tkinter GUI window
window = tk.Tk()
window.title("Shortest Path Finder on Romanian Map")

# Create a frame for dropdown menus and the button
control_frame = tk.Frame(window)
control_frame.pack(pady=10)

# Dropdowns for selecting start and end cities
start_var = tk.StringVar()
end_var = tk.StringVar()

start_label = tk.Label(control_frame, text="Start City:")
start_label.grid(row=0, column=0, padx=5)
start_menu = ttk.Combobox(control_frame, textvariable=start_var, values=list(romania_map.keys()))
start_menu.set("Select Start City")
start_menu.grid(row=0, column=1, padx=5)

end_label = tk.Label(control_frame, text="Destination City:")
end_label.grid(row=0, column=2, padx=5)
end_menu = ttk.Combobox(control_frame, textvariable=end_var, values=list(romania_map.keys()))
end_menu.set("Select Destination City")
end_menu.grid(row=0, column=3, padx=5)

# Button to start the search
search_button = tk.Button(control_frame, text="Find Shortest Path", command=lambda: show_shortest_path())
search_button.grid(row=0, column=4, padx=5)

# Canvas to draw the map
canvas = tk.Canvas(window, width=800, height=800, bg="white")
canvas.pack()

# Draw cities and roads
for city, neighbors in romania_map.items():
    x, y = city_positions[city]
    canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black", tags=city)
    canvas.create_text(x, y - 15, text=city, font=("Arial", 10))

    # Draw roads (edges)
    for neighbor, distance in neighbors.items():
        nx, ny = city_positions[neighbor]
        canvas.create_line(x, y, nx, ny, fill="gray", tags=f"{city}-{neighbor}")

# Dijkstra's algorithm to find the shortest path
def dijkstra(graph, start, goal):
    queue = PriorityQueue()
    queue.put((0, start, [start]))  # (distance, current_city, path)
    visited = set()

    while not queue.empty():
        (dist, current, path) = queue.get()
        if current in visited:
            continue
        visited.add(current)

        # Goal found
        if current == goal:
            return path, dist

        # Explore neighbors
        for neighbor, distance in graph[current].items():
            if neighbor not in visited:
                queue.put((dist + distance, neighbor, path + [neighbor]))

    return None, float('inf')  # No path found

# Start the search and display the path
def show_shortest_path():
    start = start_var.get()
    end = end_var.get()

    if start == "Select Start City" or end == "Select Destination City":
        messagebox.showerror("Error", "Please select both start and destination cities.")
        return

    # Run Dijkstra's algorithm to find the shortest path
    path, total_distance = dijkstra(romania_map, start, end)

    if path is None:
        messagebox.showinfo("Result", f"No path found from {start} to {end}")
    else:
        # Display the path visually
        for i in range(len(path) - 1):
            city = path[i]
            next_city = path[i + 1]

            # Highlight cities and roads in the path
            canvas.itemconfig(city, fill="blue")
            canvas.itemconfig(f"{city}-{next_city}", fill="blue")
            canvas.itemconfig(f"{next_city}-{city}", fill="blue")
            window.update()
            time.sleep(0.5)

        # Show total distance in a message box
        messagebox.showinfo("Result", f"Shortest path from {start} to {end}: {' -> '.join(path)}\nTotal distance: {total_distance} km")

# Run the GUI
window.mainloop()

