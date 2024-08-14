import pw_manager as pw
import os
from tkinter import *
from tkinter import ttk

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)

def click_email(email):
    copy_to_clipboard(email)

def click_pw(pw):
    copy_to_clipboard(pw)

# Function to update the scroll region of the canvas
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(canvas_window, width=canvas.winfo_width())

# Bind mouse scroll events to the canvas
def on_mouse_wheel(event):
    if event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")
    elif event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")

key = b'test\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c'

script_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file = 'credentials.i_just_discovered_i_can_give_whatever_file_extension_i_want'  #can be opened with a text editor of your choice
# Load credentials from the JSON file using the imported function
credentials = pw.load_credentials()

credentials.pop(0)

root = Tk()
root.title('Bitwarden at home GUI')

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

# Configure the main grid
root.grid_rowconfigure(2, weight=1)  # Allow row 2 (list) to expand
root.grid_columnconfigure(0, weight=1)  # Allow column 0 (main content) to expand

# Credentials label
credentials_label = Label(root, text="Credentials", font=("Helvetica", 14), anchor="w")
credentials_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Frame for the credentials list and scrollbar
list_frame = Frame(root)
list_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

# Add scrollbar to the list frame
scrollbar = Scrollbar(list_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Create a canvas to hold the credential items and attach it to the scrollbar
canvas = Canvas(list_frame, yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.config(command=canvas.yview)

# Create a frame inside the canvas to hold the actual content
content_frame = Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

content_frame.bind("<Configure>", on_frame_configure)

canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows and Linux scroll
canvas.bind_all("<Button-4>", on_mouse_wheel)   # For MacOS, up scroll
canvas.bind_all("<Button-5>", on_mouse_wheel)   # For MacOS, down scroll

# Add credential items to the content frame using data from the JSON file
for item in credentials:
    item[1] = pw.decrypt_data(key, item[1])
    item[2] = pw.decrypt_data(key, item[2])
    item[3] = pw.decrypt_data(key, item[3])

    item_frame = Frame(content_frame, bd=1, relief="solid")
    item_frame.pack(fill="x", padx=5, pady=2)

    label1 = Label(item_frame, text=item[1], font=("Helvetica", 12), anchor="w")
    label1.grid(row=0, column=0, padx=5, pady=0, sticky="w")

    label2 = Label(item_frame, text=item[2], font=("Helvetica", 8), anchor="w")
    label2.grid(row=1, column=0, padx=5, pady=2, sticky="w")

    button1 = Button(item_frame, text="@", command=lambda email=item[2]: click_email(email))
    button1.grid(row=0, column=1, rowspan=2, padx=2, pady=2, sticky="e")

    button2 = Button(item_frame, text="⚿", command=lambda pw=item[3]: click_pw(pw))
    button2.grid(row=0, column=2, rowspan=2, padx=2, pady=2, sticky="e")

    # Configure columns to stretch
    item_frame.grid_columnconfigure(0, weight=1)

# Start the Tkinter event loop
root.mainloop()
