import pyperclip
import time

def monitor_clipboard():
    """Monitor clipboard for new text."""
    print("Monitoring clipboard for text...")
    previous_text = ""
    while True:
        try:
            # Get current clipboard content
            current_text = pyperclip.paste()
            if current_text != previous_text:
                first_line = current_text.splitlines()[0] if current_text else ""
                if first_line.startswith("HEADER"):
                    print(f"Trigger detected: {first_line}")
                    process_text(current_text)
                previous_text = current_text
            time.sleep(1)  # Check every second
        except KeyboardInterrupt:
            print("Stopped monitoring clipboard.")
            break

def process_text(text):
    """Process the text from clipboard."""
    print(f"Processing text: {text}")
    # Add logic to send text to GitHub Copilot or handle it as needed

if __name__ == "__main__":
    monitor_clipboard()
