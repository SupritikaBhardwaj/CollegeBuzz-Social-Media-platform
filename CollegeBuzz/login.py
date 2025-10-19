import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import dashboard  # your dashboard.py file

# -------------------- DATABASE CONNECTION --------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="socialmedia",
        password="pass123",
        database="collegebuzz"
    )
    cursor = conn.cursor()
    print("Connected to MySQL database successfully!")
except Exception as e:
    print("Error connecting to MySQL:", e)
    exit()

# -------------------- LOGIN FUNCTION --------------------
def login():
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login", f"Welcome {username}!")
        root.destroy()  # Close login window
        dashboard.open_feed(username)
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# -------------------- REGISTER FUNCTION --------------------
def register():
    username = simpledialog.askstring("Register", "Enter username:")
    email = simpledialog.askstring("Register", "Enter email:")
    password = simpledialog.askstring("Register", "Enter password:")

    if not username or not email or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", str(e))

# -------------------- GUI SETUP --------------------
root = tk.Tk()
root.title("CollegeBuzz")
root.geometry("450x350")
root.resizable(False, False)
root.configure(bg="#f2f2f2")

# ---------- Heading ----------
heading = tk.Label(root, text="Welcome to CollegeBuzz", font=("Helvetica", 20, "bold"), bg="#f2f2f2", fg="#2c3e50")
heading.pack(pady=20)

# ---------- Username ----------
frame_username = tk.Frame(root, bg="#f2f2f2")
frame_username.pack(pady=5, padx=20, fill="x")
label_username = tk.Label(frame_username, text="Username:", font=("Arial", 12), bg="#f2f2f2", anchor="w")
label_username.pack(fill="x")
entry_username = tk.Entry(frame_username, font=("Arial", 12))
entry_username.pack(fill="x", pady=5)

# ---------- Password ----------
frame_password = tk.Frame(root, bg="#f2f2f2")
frame_password.pack(pady=5, padx=20, fill="x")
label_password = tk.Label(frame_password, text="Password:", font=("Arial", 12), bg="#f2f2f2", anchor="w")
label_password.pack(fill="x")
entry_password = tk.Entry(frame_password, font=("Arial", 12), show="*")
entry_password.pack(fill="x", pady=5)

# ---------- Buttons ----------
frame_buttons = tk.Frame(root, bg="#f2f2f2")
frame_buttons.pack(pady=20)

login_btn = tk.Button(frame_buttons, text="Login", font=("Arial", 14, "bold"), bg="#3498db", fg="white",
                      activebackground="#2980b9", width=15, command=login)
login_btn.grid(row=0, column=0, padx=10)

register_btn = tk.Button(frame_buttons, text="Create Account", font=("Arial", 14, "bold"), bg="#2ecc71", fg="white",
                         activebackground="#27ae60", width=15, command=register)
register_btn.grid(row=0, column=1, padx=10)

root.mainloop()
