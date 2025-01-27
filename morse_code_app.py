import tkinter as tk
from tkinter import ttk
import random
import winsound
import time
import threading

# Constants
CHALLENGE_ENCODE = 1
CHALLENGE_DECODE = 2
CHALLENGE_AUDIO = 3

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', "'": '.----.', ' ': '/'
}

RANDOM_PHRASES = [
    "HELLO", "WORLD", "PYTHON", "MORSE CODE", "OPENAI", "SOS", "KEEP LEARNING",
    "GOOD LUCK", "HAVE FUN", "LOVE LIFE", "LEARN CODE", "STAY SAFE", "NEVER GIVE UP",
    "HELLO WORLD", "MORSE IS COOL", "LEARNING IS FUN", "CLOUD COMPUTING", "AI IS THE FUTURE",
    "GREAT JOB", "YOU DID IT", "HAPPY CODING", "PROGRAMMING", "DEVELOPER", "MACHINE LEARNING",
    "ENJOY YOUR DAY", "ALWAYS BE KIND", "STAY POSITIVE", "WORK HARD", "MAKE IT HAPPEN",
    "HELLO THERE", "WHAT'S UP", "LET'S CODE", "GOOD MORNING", "HAVE A NICE DAY", "ENJOY THE RIDE",
    "ALWAYS LEARN", "NEVER STOP", "STAY STRONG", "PEACE AND LOVE", "FUTURE TECH", "GO FOR IT",
    "STAY CURIOUS", "BE BOLD", "HARD WORK PAYS", "SUCCESS AWAITS", "EXCEL IN EVERYTHING", 
    "NEVER LOOK BACK", "LEAD THE WAY", "THINK BIG", "MAKE A DIFFERENCE", "CHASE YOUR DREAMS",
    "DON'T GIVE UP", "BELIEVE IN YOURSELF", "TIME IS PRECIOUS", "THE SKY'S THE LIMIT",
    "MAKE IT COUNT", "FOLLOW YOUR PASSION", "DO IT TODAY", "YOU'RE AMAZING", "DON'T LOOK BACK", 
    "ALEX50 IS A BITCH", "MILES IS A BLOBFISH", "PLEASE DO NOT FEED THE WHORES DRUGS", "GAMBLING IS FUN",

]

class MorseCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Practice")
        self.root.geometry("600x600")  # Adjusted window size
        self.root.resizable(True, True)  # Allow window to be resizable
        self.current_challenge = 0

        # Main Frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid to make everything responsive
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_rowconfigure(5, weight=2)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)

        # Title Label
        title_label = ttk.Label(main_frame, text="Morse Code Practice", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        # Challenge Label
        self.challenge_label = ttk.Label(main_frame, text="Press a button to generate a challenge!", font=("Arial", 16), wraplength=500)
        self.challenge_label.grid(row=1, column=0, columnspan=3, pady=15, sticky="nsew")

        # Input Section
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")

        self.input_entry = ttk.Entry(input_frame, width=30, font=("Arial", 14), justify="center")
        self.input_entry.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.submit_button = ttk.Button(input_frame, text="Submit", command=self.submit_answer)
        self.submit_button.grid(row=0, column=1, padx=10, pady=5)

        # Buttons Section
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=15, sticky="ew")

        self.encode_button = ttk.Button(buttons_frame, text="Generate Encode", command=self.generate_encode_challenge)
        self.encode_button.grid(row=0, column=0, padx=15, pady=5, sticky="ew")

        self.decode_button = ttk.Button(buttons_frame, text="Generate Decode", command=self.generate_decode_challenge)
        self.decode_button.grid(row=0, column=1, padx=15, pady=5, sticky="ew")

        self.sound_only_button = ttk.Button(buttons_frame, text="Sound Only", command=self.sound_only_challenge)
        self.sound_only_button.grid(row=0, column=2, padx=15, pady=5, sticky="ew")

        self.toggle_chart_button = ttk.Button(buttons_frame, text="Show Morse Code Chart", command=self.toggle_chart)
        self.toggle_chart_button.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

        # Result Label
        self.result_label = ttk.Label(main_frame, text="", font=("Arial", 14), foreground="green")
        self.result_label.grid(row=4, column=0, columnspan=3, pady=10, sticky="nsew")

        # History Section
        history_frame = ttk.Frame(main_frame)
        history_frame.grid(row=5, column=0, columnspan=3, pady=20, sticky="nsew")

        self.encode_history_label = ttk.Label(history_frame, text="Encode History", font=("Arial", 14))
        self.encode_history_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.encode_history_box = tk.Listbox(history_frame, height=10, width=50, font=("Arial", 12))
        self.encode_history_box.grid(row=1, column=0, padx=10, pady=5)

        self.decode_history_label = ttk.Label(history_frame, text="Decode History", font=("Arial", 14))
        self.decode_history_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.decode_history_box = tk.Listbox(history_frame, height=10, width=50, font=("Arial", 12))
        self.decode_history_box.grid(row=1, column=1, padx=10, pady=5)

        self.sound_only_history_label = ttk.Label(history_frame, text="Sound Only History", font=("Arial", 14))
        self.sound_only_history_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.sound_only_history_box = tk.Listbox(history_frame, height=10, width=50, font=("Arial", 12))
        self.sound_only_history_box.grid(row=1, column=2, padx=10, pady=5)

        # Morse Chart Frame
        self.show_chart = False
        self.chart_frame = None

    def generate_morse_challenge(self, type):
        self.current_phrase = random.choice(RANDOM_PHRASES)
        self.input_entry.delete(0, tk.END)
        self.result_label.config(text="")

        match type:
            case 1: # CHALLENGE_ENCODE
                self.challenge_label.config(text=f"Encode: {self.current_phrase}")
            case 2: # CHALLENGE_DECODE
                morse_code = text_to_morse(self.current_phrase)
                self.challenge_label.config(text=f"Decode: {morse_code}")
            case 3: # CHALLENGE_AUDIO
                morse_code = text_to_morse(self.current_phrase)
                self.challenge_label.config(text="Audio")
                self.sound_only_button.config(state="disabled")

                # Play sound for the morse code in a background thread
                thread = threading.Thread(target=self.play_morse_code_sound, args=(morse_code,))
                thread.daemon = True  # Ensure the thread exits when the app closes
                thread.start()



    def generate_encode_challenge(self):
        self.current_challenge = CHALLENGE_ENCODE
        self.generate_morse_challenge(self.current_challenge)

    def generate_decode_challenge(self):
        self.current_challenge = CHALLENGE_DECODE
        self.generate_morse_challenge(self.current_challenge)

    def sound_only_challenge(self):
        self.current_challenge = CHALLENGE_AUDIO
        self.generate_morse_challenge(self.current_challenge)

    def play_morse_code_sound(self, morse_code):
        unit_time = 200  # Time duration of each dot/dash in milliseconds
        for symbol in morse_code:
            if symbol == '.':
                winsound.Beep(1000, 200)  # Dot sound (1000 Hz, 200 ms)
            elif symbol == '-':
                winsound.Beep(1000, 600)  # Dash sound (1000 Hz, 600 ms)
            elif symbol == ' ':
                time.sleep(200 / 1000)  # Space between parts of the same letter
            elif symbol == '/':
                time.sleep(600 / 1000)  # Space between words

        self.sound_only_button.config(state="normal")

    def toggle_chart(self):
        if self.show_chart:
            self.chart_frame.destroy()
            self.chart_frame = None
            self.toggle_chart_button.config(text="Show Morse Code Chart")
        else:
            self.chart_frame = ttk.Frame(self.root, padding="10")
            self.chart_frame.pack(pady=20)

            # Display Morse Code Chart in a Grid
            keys = list(MORSE_CODE_DICT.keys())
            for i, key in enumerate(keys):
                label_key = ttk.Label(self.chart_frame, text=key, font=("Arial", 12), width=5, anchor="center", relief="solid", background="white")
                label_value = ttk.Label(self.chart_frame, text=MORSE_CODE_DICT[key], font=("Arial", 12), width=10, anchor="center", relief="solid", background="white")
                label_key.grid(row=i // 6, column=(i % 6) * 2, padx=5, pady=5)
                label_value.grid(row=i // 6, column=(i % 6) * 2 + 1, padx=5, pady=5)

            self.toggle_chart_button.config(text="Hide Morse Code Chart")

        self.show_chart = not self.show_chart

    def submit_answer(self):
        user_input = self.input_entry.get().strip()
        correct_answer = ""
        challenge_text = self.challenge_label.cget("text")
        answer_status = ""

        match self.current_challenge:
            case 1: # CHALLENGE_ENCODE
                correct_answer = text_to_morse(self.current_phrase)
            case 2: # CHALLENGE_DECODE
                correct_answer = self.current_phrase
            case 3: # CHALLENGE_AUDIO
                correct_answer = self.current_phrase

        if user_input.upper() == correct_answer:
            self.result_label.config(text="Correct!", foreground="green")
            answer_status = "Correct"
        else:
            self.result_label.config(text="Incorrect. Try Again.", foreground="red")
            answer_status = "Incorrect"

        # Update History with result
        if "Decode:" in challenge_text:
            self.decode_history_box.insert(tk.END, f"Morse: {text_to_morse(self.current_phrase)} | Your Input: {user_input} | {answer_status}")
        elif "Encode:" in challenge_text:
            self.encode_history_box.insert(tk.END, f"Phrase: {self.current_phrase} | Your Input: {user_input} | {answer_status}")
        elif "Sound Only" in challenge_text:
            self.sound_only_history_box.insert(tk.END, f"Sound: {text_to_morse(self.current_phrase)} | Your Input: {user_input} | {answer_status}")

# Utility Function
def text_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MorseCodeApp(root)
    root.mainloop()
