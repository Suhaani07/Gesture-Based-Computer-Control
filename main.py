import tkinter as tk
import subprocess

def run_python_file(file_path):
    try:
        subprocess.run(["python", file_path], check=True)
    except subprocess.CalledProcessError as e:
        label.config(text=f"Error: {e}")

def on_head_tilt():
    run_python_file("Facetilt.py")

def on_hand_gesture():
    run_python_file("Handcontrol.py")

def open_gesture_mouse():
    run_python_file("Mouse.py")

def enable_voice_commands():
    run_python_file("voice.py")

def open_canvas():
    run_python_file("canvas-easy.py")

# Create the main application window
app = tk.Tk()
app.title("Multifunctional Buttons")

# Create a label widget
label = tk.Label(app, text="Click a button to execute a Python file", font=("Helvetica", 16))
label.pack(pady=20)

# Create buttons for different functionalities
buttons = [
    ("Head Tilt Volume", on_head_tilt),
    ("Hand Gesture Volume & Brightness", on_hand_gesture),
    ("Gesture-Based Mouse", open_gesture_mouse),
    ("Enable Voice Commands", enable_voice_commands),
    ("Open Canvas for Writing", open_canvas)
]

for btn_text, btn_command in buttons:
    btn = tk.Button(app, text=btn_text, command=btn_command)
    btn.pack(pady=10)

# Start the Tkinter event loop
app.mainloop()
