import pw_manager as pw
import os
import hashlib
from tkinter import *
from tkinter import ttk

try:
    from Crypto.Cipher import AES
    from Crypto import Random
    from Crypto.Util.Padding import pad, unpad
except ModuleNotFoundError:
    os.system('pip install pycryptodome' if os.name == 'nt' else 'pip3 install pycryptodome')

os.system('cls' if os.name == 'nt' else 'clear')

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)

def click_email(email):
    copy_to_clipboard(email)

def click_pw(pw):
    copy_to_clipboard(pw)

# function that updates the scroll region of the canvas
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(canvas_window, width=canvas.winfo_width())

# binds mouse scroll events to the canvas
def on_mouse_wheel(event):
    if event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")
    elif event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")

# sign in window that appears when no credentials file is found
def signin():
    # sign in window layout
    signin_window = Toplevel(root)
    signin_window.title("Sign In")

    Label(signin_window, text="Choose a main password:").pack(pady=5)
    main_pw_entry = Entry(signin_window, show="*", width=30)
    main_pw_entry.pack(pady=5)

    Label(signin_window, text="Confirm your password:").pack(pady=5)
    confirm_pw_entry = Entry(signin_window, show="*", width=30)
    confirm_pw_entry.pack(pady=5)

    error_label = Label(signin_window, text="", fg="red")
    error_label.pack(pady=5)

    def set_password():  # stores the hash of the main pw to the new credentials file
        main_pw = main_pw_entry.get()
        pw_confirm = confirm_pw_entry.get()
        if main_pw == pw_confirm:
            pw.save_credentials(None, 'Bitwarden at home', 'Bitwarden at home', sha256(main_pw))
            signin_window.destroy()
            login()  # prompts the user to the login window right after signing in
        else:
            error_label.config(text="The two passwords must match.")

    Button(signin_window, text="Set Password", command=set_password).pack(pady=20)
    signin_window.bind('<Return>', lambda event: set_password())

# login window that appears when a credentials file is found
def login():
    login_window = Toplevel(root)
    login_window.title("Login")

    Label(login_window, text="Insert your main password:").pack(pady=5)
    pw_entry = Entry(login_window, show="*", width=30)
    pw_entry.pack()

    error_label = Label(login_window, text="", fg="red")
    error_label.pack(pady=5)

    def verify_password():  # checks if the sha256 of the inserted password matches the one already stored
        key = pw_entry.get()
        pws = pw.load_credentials()
        if sha256(key) == pws[0][3]:
            global key_bytes
            key_bytes = pad(key.encode('utf-8'), AES.block_size)
            login_window.destroy()
            load_main_application()
        else:
            error_label.config(text="Incorrect password. Please try again.")

    Button(login_window, text="Login", command=verify_password).pack(pady=20)
    login_window.bind('<Return>', lambda event: verify_password())

# loads the main application
def load_main_application():
    global canvas, canvas_window, content_frame, credentials, search_var
    root.title('Bitwarden at home GUI')

    mainframe = ttk.Frame(root, padding='3 3 12 12')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Credentials label
    credentials_label = Label(root, text="Credentials", font=("Helvetica", 14), anchor="w")
    credentials_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Search bar and buttons frame
    search_frame = Frame(root)
    search_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    search_var = StringVar()
    search_bar = Entry(search_frame, textvariable=search_var, width=25)
    search_bar.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

    add_button = Button(search_frame, text="+", command=add_new_credentials)
    add_button.pack(side=LEFT)

    search_var.trace("w", lambda name, index, mode: update_credential_list())

    list_frame = Frame(root)
    list_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

    # adds a scrollbar that lets the user scroll through the credentials
    scrollbar = Scrollbar(list_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    canvas = Canvas(list_frame, yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=canvas.yview)

    content_frame = Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

    content_frame.bind("<Configure>", on_frame_configure)

    # binds the scroll-wheel and touchpad scroll gesture input to the scrolling action
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind_all("<Button-4>", on_mouse_wheel)
    canvas.bind_all("<Button-5>", on_mouse_wheel)

    credentials = pw.load_credentials()
    credentials.pop(0)

    update_credential_list()

# updates the list of shown credentials based on what's written in the search bar
def update_credential_list():
    global content_frame, credentials
    search_text = search_var.get().lower()

    for widget in content_frame.winfo_children():
        widget.destroy()

    for item in credentials:
        name = pw.decrypt_data(key_bytes, item[1]).lower()
        email = pw.decrypt_data(key_bytes, item[2]).lower()

        if search_text in name or search_text in email:
            item_frame = Frame(content_frame, bd=1, relief="solid")
            item_frame.pack(fill="x", padx=5, pady=2)

            label1 = Label(item_frame, text=name, font=("Helvetica", 12), anchor="w")
            label1.grid(row=0, column=0, padx=5, pady=0, sticky="w")

            label2 = Label(item_frame, text=email, font=("Helvetica", 8), anchor="w")
            label2.grid(row=1, column=0, padx=5, pady=2, sticky="w")

            button1 = Button(item_frame, text="@", command=lambda email=item[2]: click_email(pw.decrypt_data(key_bytes, email)))
            button1.grid(row=0, column=1, rowspan=2, padx=2, pady=2, sticky="e")

            button2 = Button(item_frame, text="⚿", command=lambda password=item[3]: click_pw(pw.decrypt_data(key_bytes, password)))
            button2.grid(row=0, column=2, rowspan=2, padx=2, pady=2, sticky="e")

            item_frame.grid_columnconfigure(0, weight=1)

# function to add new credentials
def add_new_credentials():
    new_window = Toplevel(root)
    new_window.title("Add New Credentials")

    Label(new_window, text="Service Name:").pack(pady=5)
    service_name_entry = Entry(new_window, width=30)
    service_name_entry.pack(pady=5)

    Label(new_window, text="Username:").pack(pady=5)
    username_entry = Entry(new_window, width=30)
    username_entry.pack(pady=5)

    Label(new_window, text="Password:").pack(pady=5)
    password_entry = Entry(new_window, show="*", width=30)
    password_entry.pack(pady=5)

    def save_credentials():
        name = service_name_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        if name and username and password:
            pw.save_credentials(key_bytes, name, username, password)
            new_window.destroy()
            credentials.append([len(credentials), pw.encrypt_data(key_bytes, name), pw.encrypt_data(key_bytes, username), pw.encrypt_data(key_bytes, password)])
            update_credential_list()

    button_frame = Frame(new_window)
    button_frame.pack(pady=10)

    cancel_button = Button(button_frame, text="Cancel", command=new_window.destroy)
    cancel_button.pack(side=LEFT, padx=5)

    save_button = Button(button_frame, text="Save", command=save_credentials)
    save_button.pack(side=RIGHT, padx=5)

# starts the Tkinter event loop
if __name__ == '__main__':
    root = Tk()
    root.geometry('400x300')

    credentials_file = 'credentials.i_just_discovered_i_can_give_whatever_file_extension_i_want'

    if not os.path.exists(credentials_file):
        signin()
    else:
        login()

    root.mainloop()
