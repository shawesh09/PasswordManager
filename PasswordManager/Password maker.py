import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import datetime
import secrets
import string
import cairo
import os
import sys
import sqlite3
from PIL import Image, ImageDraw, ImageTk

WINDOW_WIDTH = 420
WINDOW_HEIGHT = 600
rights_text = "© 2025 Abdo Shawesh. All rights reserved."

class RoundedRectangle(tk.Canvas):
    def __init__(self, parent, width, height, radius, color, text, font_style):
        super().__init__(parent, width=width, height=height, bd=0, highlightthickness=0)
        self.width = width
        self.height = height
        self.radius = radius
        self.color = color
        self.text = text
        self.font_style = font_style
        self.bind("<Configure>", self.draw_rounded_rect)
    def draw_rounded_rect(self, event=None):
        self.delete("all")

        # Create a Cairo surface and context
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(surface)

        # Draw the rounded rect
        ctx.set_source_rgb(*self.color)
        x, y, w, h, r = 0, 0, self.width, self.height, self.radius

        ctx.new_sub_path()
        ctx.arc(x + w - r, y + r, r, -0.5 * cairo.M_PI, 0)
        ctx.arc(x + w - r, y + h - r, r, 0, 0.5 * cairo.M_PI)
        ctx.arc(x + r, y + h - r, r, 0.5 * cairo.M_PI, cairo.M_PI)
        ctx.arc(x + r, y + r, r, cairo.M_PI, 1.5 * cairo.M_PI)
        ctx.close_path()
        ctx.fill()

        # Draw the text on top
        ctx.set_source_rgb(1.0, 1.0, 1.0)  # White color for text
        ctx.select_font_face(self.font_style[0], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(self.font_style[1])

        text_extents = ctx.text_extents(self.text)
        text_x = (self.width - text_extents.width) / 2
        text_y = (self.height + text_extents.height) / 2
        ctx.move_to(text_x, text_y)
        ctx.show_text(self.text)

        # Convert Cairo surface to a Tkinter PhotoImage
        image_bytes = surface.get_data()
        self.tk_image = tk.PhotoImage(width=self.width, height=self.height)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def create_rounded_rectangle(width, height, radius, color):
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    r_hex = color[1:3]
    g_hex = color[3:5]
    b_hex = color[5:7]
    rgb_color = (int(r_hex, 16), int(g_hex, 16), int(b_hex, 16))

    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=rgb_color)
    return ImageTk.PhotoImage(img)
def create_rounded_button_image(width, height, radius, color, active_color):
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    rgb_color = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=rgb_color)
    default_img = ImageTk.PhotoImage(img)

    # Create the active (clicked) button image
    active_img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(active_img)
    active_rgb_color = tuple(int(active_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=active_rgb_color)
    active_img_tk = ImageTk.PhotoImage(active_img)

    return default_img, active_img_tk

# ---------- Password Functions ----------
def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    charset = ""
    if use_upper:
        charset += string.ascii_uppercase
    if use_lower:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += "!@#$%^&*()-_=+[]{};:,.<>/?|\\"
    if not charset:
        return None

    # ensure at least one of each selected type
    passwd_chars = []
    if use_upper:
        passwd_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        passwd_chars.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        passwd_chars.append(secrets.choice(string.digits))
    if use_symbols:
        passwd_chars.append(secrets.choice("!@#$%^&*()-_=+[]{};:,.<>/?|\\"))

    while len(passwd_chars) < length:
        passwd_chars.append(secrets.choice(charset))

    secrets.SystemRandom().shuffle(passwd_chars)
    return "".join(passwd_chars[:length])
def create_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Create the passwords table with name, password, and creation_time columns
        c.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                name TEXT PRIMARY KEY,
                password TEXT UNIQUE,
                creation_time TEXT
            )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to create database: {e}")
    finally:
        if conn:
            conn.close()
def save_password():
    password_to_save = result_var.get()
    if not password_to_save:
        messagebox.showwarning("No Password", "Please generate a password first.")
        return

    password_name = simpledialog.askstring("Password Name", "Enter a name for this password:")
    if not password_name:
        return

    db_path = resource_path("resources/data/passwords.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Call the new function to ensure the database and table exist
    create_database(db_path)

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Check for existing name
        c.execute("SELECT name FROM passwords WHERE name=?", (password_name,))
        if c.fetchone():
            messagebox.showwarning("Duplicate Name",
                                   f"The name '{password_name}' already exists. Please choose a different name.")
            return

        # Check for existing password
        c.execute("SELECT password FROM passwords WHERE password=?", (password_to_save,))
        if c.fetchone():
            messagebox.showwarning("Duplicate Password", "This password already exists in the database.")
            return

        # Get the current time and format it
        current_time = datetime.datetime.now().strftime("%I:%M %p %d/%m/%Y")

        # Insert the new password with its creation time
        c.execute("INSERT INTO passwords (name, password, creation_time) VALUES (?, ?, ?)",
                  (password_name, password_to_save, current_time))

        conn.commit()
        messagebox.showinfo("Saved", f"Password for '{password_name}' saved successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to save password: {e}")
    finally:
        if conn:
            conn.close()


def show_saved_passwords():
    # Clear the current content
    for widget in passwords_list_frame.winfo_children():
        widget.destroy()

    db_path = resource_path("resources/data/passwords.db")
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Fetch passwords with creation time
        c.execute("SELECT name, password, creation_time FROM passwords ORDER BY name")
        rows = c.fetchall()

        if not rows:
            no_pass_label = tk.Label(passwords_list_frame, text="No saved passwords found.", bg="white",
                                     font=("Arial", 11))
            no_pass_label.pack(pady=10)
            return

        for name, password, creation_time in rows:
            # The parent of the grid widgets is entry_frame. We need to pack the entry_frame itself.
            entry_frame = tk.Frame(passwords_list_frame, bg="#e6e6e6", relief="solid", bd=1)
            entry_frame.pack(fill="both", padx=10, pady=5)  # Correctly pack the outer frame

            # Configure columns inside the entry_frame for horizontal filling
            entry_frame.grid_columnconfigure(0, weight=1)  # Name and Password labels will share this space
            entry_frame.grid_columnconfigure(1, weight=0)  # Time label has fixed size

            # Name and Password Labels
            name_label = tk.Label(entry_frame, text=name, font=("Arial", 12, "bold"), bg="#e6e6e6")
            pass_label = tk.Label(entry_frame, text=password, font=("Arial", 11), bg="#e6e6e6")

            # Place the labels in the first column, with the name on top of the password
            name_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
            pass_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="w")

            # Creation Time Label - Place in the second column to the right
            if creation_time:
                time_label = tk.Label(entry_frame, text=creation_time, font=("Arial", 9), bg="#e6e6e6", fg="#555")
                time_label.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="e")

            entry_frame.bind("<Button-4>", on_mouse_wheel)
            entry_frame.bind("<Button-5>", on_mouse_wheel)
            pass_label.bind("<Button-4>", on_mouse_wheel)
            pass_label.bind("<Button-5>", on_mouse_wheel)
            time_label.bind("<Button-4>", on_mouse_wheel)
            time_label.bind("<Button-5>", on_mouse_wheel)
            name_label.bind("<Button-4>", on_mouse_wheel)
            name_label.bind("<Button-5>", on_mouse_wheel)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to retrieve passwords: {e}")
    finally:
        if conn:
            conn.close()
# ---------- Main Window ----------
root = tk.Tk()
root.title("Protection Maker")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg="white")
box_width = 300
box_height = 120
corner_radius = 20
bg_color = "#7b1cff"

button_width = 200
button_height = 70
corner_radius = 35
default_color = "#b86bff"
active_color = "#a54ac7"

try:
    # Use the resource_path function if you have it
    app_icon = tk.PhotoImage(file="resources/images/cyber-security.png")
    # Set the icon for the application
    root.iconphoto(True, app_icon)
except tk.TclError:
    print("Could not load application icon.")

rounded_bg = create_rounded_rectangle(box_width, box_height, corner_radius, bg_color)

# ---- First frame (welcome page) ----
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True)

logo_frame = tk.Frame(main_frame, bg="white")
logo_frame.place(x=0, y=5)

try:
    pil_arrow_image = Image.open(resource_path("resources/images/left-arrow.png"))
    pil_arrow_image = pil_arrow_image.resize((28, 28), Image.Resampling.LANCZOS)
    back_arrow_img = ImageTk.PhotoImage(pil_arrow_image)
except (tk.TclError, FileNotFoundError):
    back_arrow_img = None
    print("Warning: Back arrow icon file not found. Falling back to text button.")
try:
    cyber_logo_img = tk.PhotoImage(file=resource_path("resources/images/cyber-security.png"))
    cyber_logo_img = cyber_logo_img.subsample(cyber_logo_img.width() // 28, cyber_logo_img.height() // 28)
except tk.TclError:
    cyber_logo_img = None
try:
    settings_icon_img = tk.PhotoImage(file=resource_path("resources/images/bookmark.png"))
    pil_image = Image.open(resource_path("resources/images/bookmark.png"))
    pil_image = pil_image.resize((28, 28), Image.Resampling.LANCZOS)  # Use LANCZOS for quality downsampling
    settings_icon_img = ImageTk.PhotoImage(pil_image)
except tk.TclError:
    settings_icon_img = None
except FileNotFoundError: # Added for robustness
    settings_icon_img = None
    print(f"Warning: Icon file not found at {resource_path('resources/images/bookmark.png')}. Falling back to text.")


if cyber_logo_img:
    # Label to hold the icon
    cyber_logo_label = tk.Label(logo_frame, image=cyber_logo_img, bg="white")
    cyber_logo_label.image = cyber_logo_img  # Keep a reference
    cyber_logo_label.pack(side="left", padx=(0, 5))

def go_to_passwords():
    main_frame.pack_forget()
    show_saved_passwords()
    passwords_frame.pack(fill="both", expand=True)
if settings_icon_img:
    # Use the image for the label
    """settings_icon = tk.Label(main_frame, image=settings_icon_img, bg="white")
    settings_icon.image = settings_icon_img  # Keep a reference"""
    show_passwords_btn = tk.Button(main_frame, image=settings_icon_img, bg="white", bd=0, relief="flat",
                                   command=go_to_passwords)
    show_passwords_btn.image = settings_icon_img  # Keep a reference
else:
    # Fallback to text if the image is not found
    """settings_icon = tk.Label(main_frame, text="⚙️", font=("Arial", 16), bg="white")"""
    show_passwords_btn = tk.Button(main_frame, text="⚙️", font=("Arial", 16), bg="white", command=go_to_passwords)
show_passwords_btn.place(relx=1.0, x=-10, y=10, anchor="ne")

logo = tk.Label(main_frame, text="Protection Maker", font=("Arial", 12, "bold"), bg="white")
logo.place(x=34, y=10)

title_box = tk.Label(main_frame, text="Welcome to the\nProtection Maker",
                     font=("Arial", 20, "bold"), fg="white",
                     image=rounded_bg, compound="center")
title_box.image = rounded_bg
title_box.place(relx=0.5, rely=0.35, anchor="center")

def go_to_options():
    main_frame.pack_forget()
    options_frame.pack(fill="both", expand=True)

start_button_img, start_button_active_img = create_rounded_button_image(
    button_width, button_height, corner_radius, default_color, active_color
)
start_button_main = tk.Button(main_frame, text="Click here\nto start",
                              font=("Arial", 14, "bold"),
                              fg="white",
                              image=start_button_img,
                              compound="center",
                              relief="flat",
                              activebackground="#a54ac7",
                              activeforeground="white",
                              command=go_to_options,
                              width=button_width,
                              height=button_height)
start_button_main.image = start_button_img
def on_button_press(event):
    start_button_main.config(image=start_button_active_img)

def on_button_release(event):
    start_button_main.config(image=start_button_img)

start_button_main.bind("<ButtonPress-1>", on_button_press)
start_button_main.bind("<ButtonRelease-1>", on_button_release)
start_button_main.active_image = start_button_active_img
start_button_main.place(relx=0.5, rely=0.55, anchor="center")

footer_label = tk.Label(main_frame,
                        text="The protection maker chooses passwords only for you\nand does not violate any privacy.\n\n" + rights_text,
                        font=("Arial", 10), bg="white", fg="black", justify="center")
footer_label.pack(side="bottom", pady=20)

# ---- Second frame (options page) ----
options_frame = tk.Frame(root, bg="white")

opt_title = tk.Label(options_frame, text="Password Options", font=("Arial", 18, "bold"), bg="white")
opt_title.pack(pady=(30,10))

# password length
length_frame = tk.Frame(options_frame, bg="white")
length_frame.pack(pady=10)
length_label = tk.Label(length_frame, text="Password length:", font=("Arial", 12), bg="white")
length_label.pack(side="left", padx=(0,10))
length_var = tk.IntVar(value=12)
length_spin = tk.Spinbox(length_frame, from_=4, to=64, textvariable=length_var, width=5, font=("Arial", 12))
length_spin.pack(side="left")

# character set options
checks_frame = tk.Frame(options_frame, bg="white")
checks_frame.pack(pady=10)

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)

cb_upper = tk.Checkbutton(checks_frame, text="Uppercase (A-Z)", variable=upper_var, bg="white", font=("Arial", 11))
cb_lower = tk.Checkbutton(checks_frame, text="Lowercase (a-z)", variable=lower_var, bg="white", font=("Arial", 11))
cb_digits = tk.Checkbutton(checks_frame, text="Digits (0-9)", variable=digits_var, bg="white", font=("Arial", 11))
cb_symbols = tk.Checkbutton(checks_frame, text="Symbols (!@#...)", variable=symbols_var, bg="white", font=("Arial", 11))

cb_upper.grid(row=0, column=0, sticky="w", padx=10, pady=3)
cb_lower.grid(row=1, column=0, sticky="w", padx=10, pady=3)
cb_digits.grid(row=0, column=1, sticky="w", padx=10, pady=3)
cb_symbols.grid(row=1, column=1, sticky="w", padx=10, pady=3)

# result box
result_frame = tk.Frame(options_frame, bg="white")
result_frame.pack(pady=20)
result_label = tk.Label(result_frame, text="Generated password:", font=("Arial", 12), bg="white")
result_label.pack(anchor="w")
result_var = tk.StringVar(value="")
result_entry = tk.Entry(result_frame, textvariable=result_var, font=("Arial", 12), width=30, justify="center")
result_entry.pack(pady=8)

# copy button
def copy_to_clipboard():
    pw = result_var.get()
    if pw:
        root.clipboard_clear()
        root.clipboard_append(pw)
        messagebox.showinfo("Copied", "Password copied to clipboard.")
    else:
        messagebox.showwarning("Empty", "No password to copy.")

copy_btn = tk.Button(result_frame, text="Copy", command=copy_to_clipboard, font=("Arial", 11))
copy_btn.pack()

# bottom frames for buttons
button_frame = tk.Frame(options_frame, bg="white")
button_frame.pack(side="bottom", pady=20)
# start button (generate password)
save_btn = tk.Button(button_frame, text="Save", font=("Arial", 12, "bold"),
                     bg="#7b1cff", fg="white", command=save_password, width=170)
def start_generate():
    length = int(length_var.get())
    pw = generate_password(length, upper_var.get(), lower_var.get(), digits_var.get(), symbols_var.get())
    if pw is None:
        messagebox.showwarning("Missing Options", "Please select at least one character set.")
        return
    result_var.set(pw)
    save_btn.pack(side="left", padx=10)

start_btn_options = tk.Button(options_frame, text="Start", font=("Arial", 12, "bold"),
                              bg="#7b1cff", fg="white", command=start_generate, width=170)
start_btn_options.pack(side="bottom", padx=10)
# back button
def go_back_main():
    options_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

if back_arrow_img:
    back_btn = tk.Button(options_frame, image=back_arrow_img, command=go_back_main, bd=0, relief="flat", bg="white")
    back_btn.image = back_arrow_img
else:
    back_btn = tk.Button(options_frame, text="Back", command=go_back_main, font=("Arial", 10))
back_btn.place(x=10, y=10)

# ----- Third Page (Saved passwords)
passwords_frame = tk.Frame(root, bg="white")

pass_title = tk.Label(passwords_frame, text="Saved Passwords", font=("Arial", 18, "bold"), bg="white")
pass_title.pack(pady=(30, 10))

passwords_list_container = tk.Frame(passwords_frame, bg="white")
passwords_list_container.pack(fill="both", expand=True, padx=10, pady=10)

# Create a canvas and a scrollbar
canvas = tk.Canvas(passwords_list_container, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(passwords_list_container, orient="vertical", command=canvas.yview)
passwords_list_frame = tk.Frame(canvas, bg="white")  # Frame to hold all password entries

# Configure the canvas to be scrollable
canvas.configure(yscrollcommand=scrollbar.set)
canvas.create_window((0, 0), window=passwords_list_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
passwords_list_frame.bind("<Configure>", on_frame_configure)

def on_mouse_wheel(event):
    if event.num == 5 or event.delta == -120:  # Check for scroll down
        canvas.yview_scroll(1, "units")
    if event.num == 4 or event.delta == 120:  # Check for scroll up
        canvas.yview_scroll(-1, "units")

passwords_list_frame.bind("<MouseWheel>", on_mouse_wheel)
passwords_list_frame.bind("<Button-4>", on_mouse_wheel)
passwords_list_frame.bind("<Button-5>", on_mouse_wheel)

scrollbar.pack(side="right", fill="both")
canvas.pack(side="left", fill="y", expand=False)

# Back button for this page
def go_back_main_from_passwords():
    passwords_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

if back_arrow_img:
    pass_back_btn = tk.Button(passwords_frame, image=back_arrow_img, command=go_back_main_from_passwords, bd=0, relief="flat", bg="white")
    pass_back_btn.image = back_arrow_img
else:
    pass_back_btn = tk.Button(passwords_frame, text="Back", command=go_back_main_from_passwords, font=("Arial", 10))
pass_back_btn.place(x=10, y=10)

root.mainloop()