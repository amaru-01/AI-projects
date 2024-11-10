import cv2
import mediapipe as mp
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Initialize MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class RockPaperScissors:
    def __init__(self):
        self.options = ["rock", "paper", "scissors"]
        self.user1_score = 0
        self.user2_score = 0
        self.computer_score = 0
        self.rounds = 0
        self.round_count = 0
        self.game_mode = "User vs Computer"
        self.user1_name = ""
        self.user2_name = ""
        self.setup_gui()
    
    def classify_gesture(self, landmarks):
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        if (index_tip.y < landmarks[6].y and middle_tip.y < landmarks[10].y and
            ring_tip.y < landmarks[14].y and pinky_tip.y < landmarks[18].y):
            return "paper"
        elif (index_tip.y < landmarks[6].y and middle_tip.y > landmarks[10].y and
              ring_tip.y > landmarks[14].y and pinky_tip.y > landmarks[18].y):
            return "scissors"
        else:
            return "rock"

   

    def display_countdown(self, frame, countdown_time):
        # Add a semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        
        # Add countdown text with better styling
        text_size = cv2.getTextSize(f"{countdown_time}", cv2.FONT_HERSHEY_DUPLEX, 4, 6)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = (frame.shape[0] + text_size[1]) // 2
        
        # Add shadow effect
        cv2.putText(frame, f"{countdown_time}", (text_x + 3, text_y + 3), 
                    cv2.FONT_HERSHEY_DUPLEX, 4, (0, 0, 0), 6)
        cv2.putText(frame, f"{countdown_time}", (text_x, text_y), 
                    cv2.FONT_HERSHEY_DUPLEX, 4, (255, 255, 255), 6)
        
        cv2.imshow("Rock Paper Scissors", frame)
        cv2.waitKey(1)

    def start_game_thread(self):
        # Disable the start button
        self.start_button.configure(state='disabled')
        
        # Create and show progress bar window
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Loading")
        self.progress_window.geometry("300x150")
        self.progress_window.transient(self.root)
        
        # Center the progress window
        window_width = 300
        window_height = 150
        screen_width = self.progress_window.winfo_screenwidth()
        screen_height = self.progress_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.progress_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Add loading label
        loading_label = ttk.Label(self.progress_window, 
                                text="Initializing game...",
                                font=('Helvetica', 10))
        loading_label.pack(pady=20)
        
        # Add progress bar
        self.progress_bar = ttk.Progressbar(self.progress_window, 
                                          length=200, 
                                          mode='determinate')
        self.progress_bar.pack(pady=10)
        
        # Start the loading process
        loading_thread = threading.Thread(target=self.load_game)
        loading_thread.start()

    def load_game(self):
        # Simulate loading process
        for i in range(101):
            time.sleep(0.03)  # Simulate some work
            self.progress_bar['value'] = i
            if i == 25:
                self.update_loading_text("Initializing camera...")
            elif i == 50:
                self.update_loading_text("Loading AI models...")
            elif i == 75:
                self.update_loading_text("Preparing game environment...")
            
            self.progress_window.update()
        
        # Close progress window and start game
        self.progress_window.destroy()
        self.start_button.configure(state='normal')
        
        # Start the actual game
        game_thread = threading.Thread(target=self.start_game)
        game_thread.start()

    def update_loading_text(self, text):
        for widget in self.progress_window.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(text=text)
                break

    def display_gesture_text(self, frame, text, position='center'):
        frame_height, frame_width = frame.shape[:2]
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 2
        thickness = 3
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

        # Calculate position based on whether it's center or side
        if position == 'center':
            text_x = (frame_width - text_size[0]) // 2
            text_y = (frame_height + text_size[1]) // 2
        elif position == 'left':
            text_x = 50
            text_y = frame_height // 2
        else:  # right
            text_x = frame_width - text_size[0] - 50
            text_y = frame_height // 2
        
        # Add background rectangle
        padding = 20
        cv2.rectangle(frame,
                     (text_x - padding, text_y - text_size[1] - padding),
                     (text_x + text_size[0] + padding, text_y + padding),
                     (0, 0, 0), -1)
        
        # Add text with shadow effect
        cv2.putText(frame, text,
                   (text_x + 2, text_y + 2),
                   font, font_scale, (0, 0, 0), thickness)
        cv2.putText(frame, text,
                   (text_x, text_y),
                   font, font_scale, (255, 255, 255), thickness)

    def start_game(self):
        self.user1_score = 0
        self.user2_score = 0
        self.computer_score = 0
        self.round_count = 0

        try:
            self.rounds = int(self.round_entry.get())
            if self.rounds <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of rounds.")
            return

        # Get player names with default values
        self.user1_name = self.user1_name_entry.get().strip() or "Player 1"
        if self.game_mode == "User vs Human":
            self.user2_name = self.user2_name_entry.get().strip() or "Player 2"

            # Show position instructions for 2-player mode
            messagebox.showinfo("Player Positions", 
                              f"{self.user1_name}: Please stand on the LEFT side of the camera\n"
                              f"{self.user2_name}: Please stand on the RIGHT side of the camera")

        # Initialize video capture with optimization
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Initialize hands with optimized parameters
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2 if self.game_mode == "User vs Human" else 1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        while self.round_count < self.rounds:
            user_gesture = None
            user2_gesture = None
            computer_gesture = random.choice(self.options) if self.game_mode == "User vs Computer" else None

            # Countdown phase
            for i in range(3, 0, -1):
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)  # Mirror the frame
                
                # Add divider and labels during countdown too
                if self.game_mode == "User vs Human":
                    frame_height, frame_width = frame.shape[:2]
                    cv2.line(frame, 
                            (frame_width // 2, 0), 
                            (frame_width // 2, frame_height), 
                            (255, 255, 255), 2)
                    
                    # Add player labels
                    cv2.rectangle(frame, (0, 0), (frame_width // 2, 40), (0, 0, 0), -1)
                    cv2.rectangle(frame, (frame_width // 2, 0), (frame_width, 40), (0, 0, 0), -1)
                    cv2.putText(frame, f"{self.user1_name}'s Side", (20, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(frame, f"{self.user2_name}'s Side", (frame_width // 2 + 20, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                
                self.display_countdown(frame, i)
                time.sleep(0.7)

            # Capture and process gesture
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            
            # Process frame with MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                if self.game_mode == "User vs Computer":
                    hand_landmarks = results.multi_hand_landmarks[0]
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    user_gesture = self.classify_gesture(hand_landmarks.landmark)
                    # Display user gesture
                    self.display_gesture_text(frame, f"You chose: {user_gesture.upper()}", 'left')
                    # Display computer gesture
                    self.display_gesture_text(frame, f"Computer chose: {computer_gesture.upper()}", 'right')
                else:  # User vs Human mode
                    if len(results.multi_hand_landmarks) >= 2:
                        # Process both hands
                        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks[:2]):
                            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            if idx == 0:
                                user_gesture = self.classify_gesture(hand_landmarks.landmark)
                                self.display_gesture_text(frame, f"{self.user1_name}: {user_gesture.upper()}", 'left')
                            else:
                                user2_gesture = self.classify_gesture(hand_landmarks.landmark)
                                self.display_gesture_text(frame, f"{self.user2_name}: {user2_gesture.upper()}", 'right')

            # Determine round result
            result_text = self.determine_winner(user_gesture, user2_gesture, computer_gesture)
            
            # Display game information
            self.display_game_info(frame, user_gesture, user2_gesture, computer_gesture, result_text)
            
            cv2.imshow("Rock Paper Scissors", frame)
            cv2.waitKey(2000)
            self.round_count += 1

        # Display final results
        self.show_final_results()
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        hands.close()

    def determine_winner(self, user_gesture, user2_gesture, computer_gesture):
        if self.game_mode == "User vs Computer":
            if not user_gesture or not computer_gesture:
                return "No gesture detected!"
            
            if (user_gesture == "rock" and computer_gesture == "scissors") or \
               (user_gesture == "paper" and computer_gesture == "rock") or \
               (user_gesture == "scissors" and computer_gesture == "paper"):
                self.user1_score += 1
                return f"{self.user1_name} Wins!"
            elif user_gesture == computer_gesture:
                return "It's a Tie!"
            else:
                self.computer_score += 1
                return "Computer Wins!"
        else:  # User vs Human
            if not user_gesture or not user2_gesture:
                return "Waiting for both players..."
            
            if (user_gesture == "rock" and user2_gesture == "scissors") or \
               (user_gesture == "paper" and user2_gesture == "rock") or \
               (user_gesture == "scissors" and user2_gesture == "paper"):
                self.user1_score += 1
                return f"{self.user1_name} Wins!"
            elif user_gesture == user2_gesture:
                return "It's a Tie!"
            else:
                self.user2_score += 1
                return f"{self.user2_name} Wins!"

    def display_game_info(self, frame, user_gesture, user2_gesture, computer_gesture, result_text):
        frame_height, frame_width = frame.shape[:2]
        
        if self.game_mode == "User vs Human":
            # Draw vertical divider line
            cv2.line(frame, 
                    (frame_width // 2, 0), 
                    (frame_width // 2, frame_height), 
                    (255, 255, 255), 2)

            # Add player labels at the top of each side
            # Player 1 side
            cv2.rectangle(frame, (0, 0), (frame_width // 2, 40), (0, 0, 0), -1)
            cv2.putText(frame, f"{self.user1_name}'s Side", 
                       (20, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.8, (255, 255, 255), 2)

            # Player 2 side
            cv2.rectangle(frame, (frame_width // 2, 0), (frame_width, 40), (0, 0, 0), -1)
            cv2.putText(frame, f"{self.user2_name}'s Side", 
                       (frame_width // 2 + 20, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.8, (255, 255, 255), 2)

        # Add semi-transparent overlay for text background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, frame_height - 80), (frame_width, frame_height), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)

        # Display round information
        cv2.putText(frame, f"Round {self.round_count + 1}/{self.rounds}", 
                    (20, frame_height - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display gestures
        if self.game_mode == "User vs Computer":
            if user_gesture:
                cv2.putText(frame, f"{self.user1_name}: {user_gesture}", 
                            (20, frame_height - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if computer_gesture:
                cv2.putText(frame, f"Computer: {computer_gesture}", 
                            (frame_width - 300, frame_height - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        else:
            if user_gesture:
                cv2.putText(frame, f"{self.user1_name}: {user_gesture}", 
                            (20, frame_height - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if user2_gesture:
                cv2.putText(frame, f"{self.user2_name}: {user2_gesture}", 
                            (frame_width - 300, frame_height - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display result text in the center
        if result_text:
            text_size = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_DUPLEX, 2, 3)[0]
            text_x = (frame_width - text_size[0]) // 2
            text_y = frame_height // 2

            # Add background rectangle for result text
            cv2.rectangle(frame, 
                         (text_x - 10, text_y - text_size[1] - 10),
                         (text_x + text_size[0] + 10, text_y + 10),
                         (0, 0, 0), -1)
            cv2.putText(frame, result_text, 
                       (text_x, text_y), 
                       cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)

    def show_final_results(self):
        if self.game_mode == "User vs Computer":
            winner = self.user1_name if self.user1_score > self.computer_score else "Computer" if self.computer_score > self.user1_score else "It's a Draw"
            messagebox.showinfo("Game Over", 
                              f"Final Score:\n{self.user1_name}: {self.user1_score}\n"
                              f"Computer: {self.computer_score}\n\n"
                              f"Winner: {winner}!")
        else:
            winner = self.user1_name if self.user1_score > self.user2_score else self.user2_name if self.user2_score > self.user1_score else "It's a Draw"
            messagebox.showinfo("Game Over", 
                              f"Final Score:\n{self.user1_name}: {self.user1_score}\n"
                              f"{self.user2_name}: {self.user2_score}\n\n"
                              f"Winner: {winner}!")

    def update_game_mode(self):
        self.game_mode = self.mode_var.get()
        if self.game_mode == "User vs Human":
            self.user2_frame.pack(after=self.user1_frame, padx=20, pady=5, fill="x")
        else:
            self.user2_frame.pack_forget()

    def setup_gui(self):
        # Configure the main window
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("400x600")
        self.root.configure(bg='#f0f0f0')

        # Create main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, 
                               text="Rock Paper Scissors", 
                               font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=20)

        # Game mode frame
        mode_frame = ttk.LabelFrame(main_frame, text="Game Mode", padding="10")
        mode_frame.pack(padx=20, pady=10, fill="x")

        self.mode_var = tk.StringVar(value="User vs Computer")
        
        # Radio buttons for game mode
        ttk.Radiobutton(mode_frame, 
                       text="User vs Computer",
                       variable=self.mode_var,
                       value="User vs Computer",
                       command=self.update_game_mode).pack(pady=5)
        
        ttk.Radiobutton(mode_frame, 
                       text="User vs Human",
                       variable=self.mode_var,
                       value="User vs Human",
                       command=self.update_game_mode).pack(pady=5)

        # Player 1 frame
        self.user1_frame = ttk.LabelFrame(main_frame, text="Player 1", padding="10")
        self.user1_frame.pack(padx=20, pady=5, fill="x")
        
        ttk.Label(self.user1_frame, text="Name:").pack()
        self.user1_name_entry = ttk.Entry(self.user1_frame)
        self.user1_name_entry.pack(pady=5, fill="x")

        # Player 2 frame (initially hidden)
        self.user2_frame = ttk.LabelFrame(main_frame, text="Player 2", padding="10")
        ttk.Label(self.user2_frame, text="Name:").pack()
        self.user2_name_entry = ttk.Entry(self.user2_frame)
        self.user2_name_entry.pack(pady=5, fill="x")

        # Rounds frame
        rounds_frame = ttk.LabelFrame(main_frame, text="Game Settings", padding="10")
        rounds_frame.pack(padx=20, pady=10, fill="x")
        
        ttk.Label(rounds_frame, text="Number of Rounds:").pack()
        self.round_entry = ttk.Entry(rounds_frame)
        self.round_entry.pack(pady=5, fill="x")
        self.round_entry.insert(0, "3")

        # Start button with styling
        style = ttk.Style()
        style.configure("Start.TButton", 
                       font=('Helvetica', 12, 'bold'),
                       padding=10)
        
        self.start_button = ttk.Button(main_frame, 
                                     text="Start Game",
                                     style="Start.TButton",
                                     command=self.start_game_thread)
        self.start_button.pack(pady=20)

        # Instructions
        instructions_frame = ttk.LabelFrame(main_frame, text="How to Play", padding="10")
        instructions_frame.pack(padx=20, pady=10, fill="x")
        
        instructions = (
            "1. Select your game mode\n"
            "2. Enter player name(s)\n"
            "3. Set number of rounds\n"
            "4. Wait for countdown and show your gesture\n"
            "5. Keep your hand steady for better detection\n"
            "6. In 2-player mode, both players show gestures simultaneously"
        )
        
        instructions_label = ttk.Label(instructions_frame, 
                                     text=instructions,
                                     wraplength=300,
                                     justify="left")
        instructions_label.pack(pady=5)

        # Version info
        version_label = ttk.Label(main_frame, 
                                text="v1.0",
                                font=('Helvetica', 8))
        version_label.pack(pady=5)

        self.root.mainloop()

if __name__ == "__main__":
    game = RockPaperScissors()