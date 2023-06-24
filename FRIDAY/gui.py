import tkinter as tk
from chat_gpt_communication import start_conversation
from tkinter import messagebox
from tkinter import simpledialog
import sys
import pyttsx3

# Store username and voice settings
profile = {
    "username": "",
    "selected_voice": 0,
    "speed": 5
}

# Read the profile from the file
try:
    with open("profile.txt", "r") as f:
        profile_data = f.read()
        if profile_data:
            profile = eval(profile_data)
except FileNotFoundError:
    pass

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get the available voices
voices = engine.getProperty('voices')

def set_voice():
    # Set the selected voice
    engine.setProperty('voice', voices[profile["selected_voice"]].id)

def activate_assistant():
    # Initialize chat with ChatGPT using transcribed user input
    start_conversation()

def quit_assistant():
    # Perform actions to quit the assistant
    with open("profile.txt", "w") as f:
        f.write(str(profile))  # Save the profile to a file
    root.destroy()  # Close the main window
    sys.exit()  # Exit the program

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    # Voice Selection
    voice_label = tk.Label(settings_window, text="Voice Selection:")
    voice_label.pack()

    voice_names = [voice.name for voice in voices]

    selected_voice = tk.StringVar()
    selected_voice.set(voice_names[profile["selected_voice"]])

    voice_option_menu = tk.OptionMenu(settings_window, selected_voice, *voice_names)
    voice_option_menu.pack()

    # Speed of Reader
    speed_label = tk.Label(settings_window, text="Speed of Reader:")
    speed_label.pack()

    speed_scale = tk.Scale(settings_window, from_=1, to=10, orient=tk.HORIZONTAL)
    speed_scale.set(profile["speed"])
    speed_scale.pack()

    # Username
    username_label = tk.Label(settings_window, text="Username:")
    username_label.pack()

    username_entry = tk.Entry(settings_window)
    username_entry.insert(tk.END, profile["username"])
    username_entry.pack()

    # Save Settings
    def save_settings():
        global profile  # Use the global keyword to access the profile dictionary

        profile["username"] = username_entry.get()
        profile["selected_voice"] = voice_names.index(selected_voice.get())
        profile["speed"] = speed_scale.get()

        with open("profile.txt", "w") as f:
            f.write(str(profile))

        messagebox.showinfo("Settings", "Settings saved successfully.")
        settings_window.destroy()

    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack()

root = tk.Tk()
root.title(f"FRIDAY ASSISTANT - {profile['username']}")
root.geometry("400x90")  # Set the initial window size
root.geometry(f"400x90+{root.winfo_screenwidth() // 2 - 350}+{root.winfo_screenheight() // 2 - 250}")  # Center the window
app = tk.Frame(root)
app.pack()

set_voice()  # Set the initial voice based on the profile

activate_button = tk.Button(app, text="Activate", command=activate_assistant)
activate_button.pack(side='left')

quit_button = tk.Button(app, text="Quit", command=quit_assistant)
quit_button.pack(side='right')

settings_button = tk.Button(app, text="Settings", command=open_settings)
settings_button.pack()

root.mainloop()
