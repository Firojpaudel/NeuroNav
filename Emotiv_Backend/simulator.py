import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time
from live_advance import LiveAdvance

# Configuration details
your_app_client_id = 'XtMIEP4zNp0XNhvjHsKWkS5JVPjShy8KlGcMNhgu'  # Replace with your Cortex client ID
your_app_client_secret = 'cv9gq02WQieE9KLSrc5ZcE5MUkqPWkvk75Np7A4jehDgv1tJyRdJOXuc57KiqPYYfSaKBAnWE2AvqDAws3ta5ivZmt4X7WNlGrYW7S81C1UKxAbtI7tMJm2obI8yWsS2'  # Replace with your Cortex client secret
trained_profile_name = 'Firoj'  # Replace with your trained profile name

# Global variables
live_advance_instance = None
action_received = None
canvas = None
wheelchair = None
wheelchair_x, wheelchair_y = 0, 0
canvas_width, canvas_height = 700, 400  # Increased canvas size
wheelchair_width, wheelchair_height = 50, 75  # Wheelchair image dimensions

def reset_position():
    """Reset the wheelchair to the center of the canvas."""
    global wheelchair_x, wheelchair_y
    target_x = (canvas_width - wheelchair_width) // 2
    target_y = (canvas_height - wheelchair_height) // 2
    animate_movement(target_x, target_y)

def animate_movement(target_x, target_y):
    """Smoothly animate the wheelchair to the target position."""
    global wheelchair_x, wheelchair_y
    steps = 20  # Number of steps for the animation
    dx = (target_x - wheelchair_x) / steps
    dy = (target_y - wheelchair_y) / steps

    for _ in range(steps):
        wheelchair_x += dx
        wheelchair_y += dy
        update_canvas()
        window.update()
        time.sleep(0.02)  # Pause briefly to create the animation effect

    # Ensure the final position is exact
    wheelchair_x, wheelchair_y = target_x, target_y
    update_canvas()

def process_command(action):
    """Simulate wheelchair movement based on the action with smooth animation."""
    global wheelchair_x, wheelchair_y
    step = 50  # Movement step size
    target_x, target_y = wheelchair_x, wheelchair_y

    if action.lower() == "push":
        if wheelchair_y - step >= 0:  # Prevent going off the top
            target_y -= step
    elif action.lower() == "pull":
        if wheelchair_y + step + wheelchair_height <= canvas_height:  # Prevent going off the bottom
            target_y += step
    else:
        update_gui("Unknown command!")
        return

    # Animate to the new position
    animate_movement(target_x, target_y)
    update_gui(f"Action performed: {action.capitalize()}")

def update_gui(message):
    """Update the GUI to display the current action."""
    movement_label.config(text=message)
    window.update()
    time.sleep(1)  # Simulate the action duration
    movement_label.config(text="Ready for next command.")

def update_canvas():
    """Update the wheelchair's position on the canvas."""
    canvas.coords(wheelchair, wheelchair_x, wheelchair_y)

def on_new_com_data(*args, **kwargs):
    """Callback to handle new mental command data from LiveAdvance."""
    data = kwargs.get('data')
    if not data:
        return

    action = data.get('action')
    power = data.get('power')

    if action and power is not None:
        print(f"Received action: {action}, Power: {power}")
        if power >= 0.14:  # Only process significant actions
            process_command(action)

def start_live_advance():
    """Start the LiveAdvance instance."""
    global live_advance_instance
    live_advance_instance = LiveAdvance(your_app_client_id, your_app_client_secret)
    live_advance_instance.on_new_com_data = on_new_com_data
    print("Starting Neuro-Controlled Wheelchair...")
    live_advance_instance.start(trained_profile_name)

def handle_manual_command():
    """Handle manual command input."""
    action = command_entry.get().strip()
    if action:
        threading.Thread(target=process_command, args=(action,)).start()
        command_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a valid command.")

# GUI Setup
window = tk.Tk()
window.title("Neuro-Controlled Wheelchair Simulator")
window.geometry(f"{canvas_width + 100}x{canvas_height + 150}")

title_label = tk.Label(window, text="Welcome to NeuroNav Training Simulator", font=("Helvetica", 16))
title_label.pack(pady=10)

movement_label = tk.Label(window, text="Ready for commands.", font=("Helvetica", 14), fg="green")
movement_label.pack(pady=10)

# Canvas for visual representation
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="lightgray")
canvas.pack(pady=10)

# Load wheelchair image
wheelchair_img = Image.open("wheelchair.jpg")  # Replace with the path to your wheelchair image
wheelchair_img = wheelchair_img.resize((wheelchair_width, wheelchair_height), Image.LANCZOS)
wheelchair_img_tk = ImageTk.PhotoImage(wheelchair_img)

# Initialize wheelchair position at the center
wheelchair_x = (canvas_width - wheelchair_width) // 2
wheelchair_y = (canvas_height - wheelchair_height) // 2
wheelchair = canvas.create_image(wheelchair_x, wheelchair_y, anchor=tk.NW, image=wheelchair_img_tk)

# Command input and buttons
command_entry = tk.Entry(window, font=("Helvetica", 12))
command_entry.pack(pady=10)

manual_command_button = tk.Button(window, text="Send Manual Command", font=("Helvetica", 12), command=handle_manual_command)
manual_command_button.pack(pady=10)

start_button = tk.Button(window, text="Start Neuro-Controlled System", font=("Helvetica", 12), 
                         command=lambda: threading.Thread(target=start_live_advance).start())
start_button.pack(pady=10)

exit_button = tk.Button(window, text="Exit", font=("Helvetica", 12), command=window.quit)
exit_button.pack(pady=10)
# Add Reset Button
reset_button = tk.Button(window, text="Reset Position", font=("Helvetica", 12), command=reset_position)
reset_button.pack(pady=10)
# Run the GUI
window.mainloop()
