import tkinter as tk
import threading
import winsound
import time
import pyttsx3

# Define Morse code dictionary
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}

# Define Morse code timing
dot_duration = 200  # Duration of a dot (ms)
dash_duration = 3 * dot_duration  # Duration of a dash (ms)
pause_duration = dot_duration  # Duration of pause between elements of a character (ms)
word_pause_duration = 7 * dot_duration  # Duration of pause between words (ms)

# Function to convert text to Morse code
def convert_to_morse():
    text = text_entry.get('1.0', tk.END).upper()
    morse = ''

    for char in text:
        if char in morse_code:
            morse += morse_code[char] + ' '
        else:
            morse += ' '

    morse_entry.delete('1.0', tk.END)
    morse_entry.insert(tk.END, morse)

# Function to convert Morse code to text
def convert_to_text():
    morse = morse_entry.get('1.0', tk.END)
    text = ''

    for code in morse.split(' '):
        for char, morse_char in morse_code.items():
            if code == morse_char:
                text += char
                break
        else:
            text += ' '

    text_entry.delete('1.0', tk.END)
    text_entry.insert(tk.END, text)


# Global variables
is_playing = False  # Flag to indicate if Morse code sound is being played
stop_requested = False  # Flag to indicate if stop has been requested

# Function to play Morse code sound
def play_morse_sound():
    global is_playing, stop_requested
    is_playing = True
    stop_requested = False

    text = morse_entry.get('1.0', tk.END)
    for char in text:
        if stop_requested:
            break

        if char == '.':
            winsound.Beep(1000, dot_duration)  # Frequency: 1000 Hz, Duration: dot_duration
        elif char == '-':
            winsound.Beep(1000, dash_duration)  # Frequency: 1000 Hz, Duration: dash_duration
        elif char == ' ':
            # Pause between characters
            time.sleep(pause_duration / 1000)
        elif char == '/':
            # Pause between words
            time.sleep(word_pause_duration / 1000)

    is_playing = False

# Function to stop playing the Morse code sound
def stop_sound():
    global stop_requested
    stop_requested = True

# Function to play Morse code sound in a separate thread
def play_sound_thread():
    global is_playing

    if is_playing:
        return

    is_playing = True

    sound_thread = threading.Thread(target=play_morse_sound)
    sound_thread.start()
    
# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to play the original English text using text-to-speech
def play_original_text():
    text = text_entry.get('1.0', tk.END).strip()
    if text:
        engine.say(text)
        engine.runAndWait()

# Create the main window
window = tk.Tk()
window.title("Morse Code Converter")

# Create labels
text_label = tk.Label(window, text="Text:")
morse_label = tk.Label(window, text="Morse Code:")

# Create text entry fields
text_entry = tk.Text(window, width=40, height=10)
morse_entry = tk.Text(window, width=40, height=10)

# Create buttons
convert_to_morse_button = tk.Button(window, text="Convert to Morse", command=convert_to_morse)
convert_to_text_button = tk.Button(window, text="Convert to Text", command=convert_to_text)
play_morse_button = tk.Button(window, text="Play Morse Code", command=play_sound_thread)
play_text_button = tk.Button(window, text="Play Original Text", command=play_original_text)
stop_sound_button = tk.Button(window, text="Stop Sound", command=stop_sound)

# Function to handle keyboard button press
def keyboard_button_press(char):
    text_entry.insert(tk.END, char)

# Create the virtual keyboard
keyboard_frame = tk.Frame(window)

# Define the keyboard buttons
keyboard_buttons = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ','],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', '-', '/']
]

# Create the keyboard buttons and associate them with the button press handler
for row, button_row in enumerate(keyboard_buttons):
    for col, char in enumerate(button_row):
        button = tk.Button(keyboard_frame, text=char, width=3, command=lambda c=char: keyboard_button_press(c))
        button.grid(row=row, column=col, padx=2, pady=2)

# Add the elements to the window using grid layout
text_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
text_entry.grid(row=0, column=1, padx=10, pady=5)
convert_to_morse_button.grid(row=0, column=2, padx=10, pady=5)
morse_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
morse_entry.grid(row=1, column=1, padx=10, pady=5)
convert_to_text_button.grid(row=1, column=2, padx=10, pady=5)
play_morse_button.grid(row=2, column=0, padx=10, pady=5)
play_text_button.grid(row=2, column=1, padx=10, pady=5)
stop_sound_button.grid(row=2, column=2, padx=10, pady=5)
keyboard_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

# Run the main window loop
window.mainloop()