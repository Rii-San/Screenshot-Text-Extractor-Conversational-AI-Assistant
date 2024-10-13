import hashlib
import tkinter as tk
import customtkinter as ctk
from PIL import ImageGrab, Image
import pytesseract
import threading
from pystray import Icon as TrayIcon, MenuItem as Item, Menu
from PIL import Image as TrayImage
import os
import time
import ollama

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global variables
previous_hash = None
window = None
extracted_text = ""
tray_icon = None
instructions = """
Could you please explain the following text?
If possible, I would also appreciate it if you could ask up to 4 relevant questions related to the topic at the end.
However, if the text does not lend itself to questions, you can skip that part. \n
    """
messages = []  # To store chat history

# Window Theme
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# Color Scheme
BG_COLOR = "#2E3440"  # Dark background
TEXT_COLOR = "#D8DEE9"  # Light text


# OCR
def extract_text_from_image(image):
    try:
        return pytesseract.image_to_string(image) if image else ""
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

# Grabbing Screenshot
def hash_image(image):
    small_image = image.resize((50, 50))
    return hashlib.md5(small_image.tobytes()).hexdigest()

def check_for_screenshot():
    global extracted_text, window, previous_hash

    while True:
        image = ImageGrab.grabclipboard()
        if image and isinstance(image, Image.Image):
            current_hash = hash_image(image)
            if current_hash != previous_hash:
                previous_hash = current_hash
                extracted_text = None
                extracted_text = instructions
                extracted_text += extract_text_from_image(image)
                extracted_text += "\n\nTUTOR:"

                # Automatically pass the extracted text to the AI with instructions
                if window is None:
                    window = create_ui()
                window.deiconify()  # Ensure the window pops up

                # Display the extracted text with the prefix "Image: "
                text_entry.configure(state=tk.NORMAL)
                text_entry.insert(tk.END, "SNAP TEXT:\n")
                text_entry.insert(tk.END, extracted_text + "\n\n")
                text_entry.see(tk.END)
                text_entry.configure(state=tk.DISABLED)

                threading.Thread(target=generate_response, args=(extracted_text,), daemon=True).start()

        time.sleep(0.2)

# Interacting with LLM
def generate_response(text):
    global messages

    # Add user message to chat history
    messages.append({
        'role': 'user',
        'content': text,
    })

    # Generate response using ollama
    stream = ollama.chat(model='mistral', messages=messages, stream=True)

    response = ""
    for chunk in stream:
        part = chunk['message']['content']
        response += part
        text_entry.configure(state=tk.NORMAL)
        text_entry.insert(tk.END, part)
        text_entry.see(tk.END)
        text_entry.update()  # Update the GUI to show the character being added
    text_entry.configure(state=tk.DISABLED)

    # Add assistant message to chat history
    messages.append({
        'role': 'assistant',
        'content': response,
    })

# Printing on Display screen
def append_text_to_chat(text: str, use_label: bool = False):
    global text_entry
    text_entry.configure(state=tk.NORMAL)
    if use_label:
        # Assuming you have a label widget to update
        cur_label_widget = None  # Replace with actual label widget
        cur_label_widget.configure(text=cur_label_widget.cget("text") + text)
    else:
        text_entry.insert(tk.END, text)
    text_entry.see(tk.END)
    text_entry.configure(state=tk.DISABLED)

# Mathematical rendering 


# Display screen
def on_input_field_enter(event):
    user_input = input_field.get().strip()
    if user_input:
        text_entry.configure(state=tk.NORMAL)
        text_entry.insert(tk.END, "\n\nYOU: ")
        text_entry.insert(tk.END, user_input + "\n\nTUTOR: \n\n")
        text_entry.see(tk.END)
        text_entry.configure(state=tk.DISABLED)
        input_field.delete(0, tk.END)
        threading.Thread(target=generate_response, args=(user_input,), daemon=True).start()

# Tray Functions 
def minimize_to_tray():
    global tray_icon
    if window.state() == 'withdrawn':
        return
    window.withdraw()

    image = TrayImage.open("icons/BAicon.png")
    menu = Menu(Item('Show', show_window_from_tray), Item('Quit', on_quit_from_tray))
    
    if tray_icon:
        tray_icon.stop()

    tray_icon = TrayIcon("Book Assistant", image, "Book Assistant", menu)
    threading.Thread(target=tray_icon.run, daemon=True).start()

def on_quit_from_tray(icon, item):
    icon.stop()
    os._exit(0)

def show_window_from_tray(icon, item):
    global window, tray_icon
    window.deiconify()
    if tray_icon:
        tray_icon.stop()
        tray_icon = None

# Main UI setup
def create_ui():
    global window, text_entry, input_field

    window = ctk.CTk()
    window.geometry('650x350')
    window.title('Book Assistance')
    window.configure(bg=BG_COLOR)
    window.protocol("WM_DELETE_WINDOW", minimize_to_tray)
    window.iconbitmap('icons/BAicon.ico')

    window.columnconfigure(0, weight=1, uniform='a')
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=0)

    text_entry = ctk.CTkTextbox(window, wrap=tk.WORD, font=('Arial', 16), fg_color=BG_COLOR, text_color=TEXT_COLOR, corner_radius=10)
    text_entry.grid(column=0, row=0, sticky='nsew', padx=10, pady=10)

    button_frame = ctk.CTkFrame(window)
    button_frame.grid(column=0, row=1, sticky='nsew')

    input_field = ctk.CTkEntry(button_frame, placeholder_text="Start Chatting...", font=('Arial', 16), width=630, height=35)
    input_field.grid(column=0, row=0, sticky='nsew', padx=(10, 0), pady=10)
    input_field.bind('<Return>', on_input_field_enter)

    return window

if __name__ == "__main__":
    window = create_ui()
    threading.Thread(target=check_for_screenshot, daemon=True).start()
    window.mainloop()