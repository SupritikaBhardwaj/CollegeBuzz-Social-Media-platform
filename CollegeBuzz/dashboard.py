import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import mysql.connector
from PIL import Image, ImageTk

# -------------------- DATABASE CONNECTION --------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="socialmedia",
        password="pass123",
        database="collegebuzz"
    )
    cursor = conn.cursor()
except Exception as e:
    print("Error connecting to MySQL:", e)
    exit()

# -------------------- DASHBOARD WINDOW --------------------
def open_feed(username):
    feed_win = tk.Tk()
    feed_win.title(f"CollegeBuzz - {username}'s Feed")
    feed_win.geometry("600x600")
    feed_win.configure(bg="#f2f2f2")

    # ---------- Header ----------
    header_frame = tk.Frame(feed_win, bg="#34495e", height=50)
    header_frame.pack(fill="x")

    header_label = tk.Label(header_frame, text=f"Welcome, {username}", font=("Helvetica", 16, "bold"), fg="white", bg="#34495e")
    header_label.pack(side="left", padx=10)

    logout_btn = tk.Button(header_frame, text="Logout", font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", command=lambda: logout(feed_win))
    logout_btn.pack(side="right", padx=10, pady=5)

    # ---------- Buttons ----------
    btn_frame = tk.Frame(feed_win, bg="#f2f2f2")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Create Post", font=("Arial", 12, "bold"), bg="#3498db", fg="white", width=15,
              command=lambda: create_post(username, feed_win)).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Post Image", font=("Arial", 12, "bold"), bg="#9b59b6", fg="white", width=15,
              command=lambda: create_image_post(username, feed_win)).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Create Poll", font=("Arial", 12, "bold"), bg="#f39c12", fg="white", width=15,
              command=lambda: create_poll(username, feed_win)).grid(row=0, column=2, padx=5)

    # ---------- Scrollable Feed ----------
    canvas = tk.Canvas(feed_win, bg="#f2f2f2")
    scrollbar = tk.Scrollbar(feed_win, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f2f2f2")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ---------- Load Posts ----------
    load_posts(scroll_frame)

    feed_win.mainloop()

# -------------------- FUNCTIONS --------------------
def logout(win):
    win.destroy()
    import login  # Return to login page

def load_posts(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    cursor.execute("""
        SELECT u.username, p.content, p.created_at
        FROM posts p
        JOIN users u ON p.user_id = u.user_id
        ORDER BY p.created_at DESC
    """)
    posts = cursor.fetchall()

    for post in posts:
        post_frame = tk.Frame(frame, bg="white", padx=10, pady=10, bd=1, relief="solid")
        post_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(post_frame, text=f"{post[0]} - {post[2]}", font=("Arial", 10, "bold"), bg="white", anchor="w").pack(fill="x")
        tk.Label(post_frame, text=post[1], font=("Arial", 12), bg="white", anchor="w", wraplength=550, justify="left").pack(fill="x", pady=5)

def create_post(username, win):
    content = simpledialog.askstring("New Post", "Write your post:")
    if content:
        cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO posts (user_id, content) VALUES (%s, %s)", (user_id, content))
        conn.commit()
        messagebox.showinfo("Posted", "Your post has been created!")
        load_posts(win.children['!canvas'].children['!frame'])  # Refresh feed

def create_image_post(username, win):
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if file_path:
        cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO posts (user_id, content) VALUES (%s, %s)", (user_id, f"[Image]: {file_path}"))
        conn.commit()
        messagebox.showinfo("Posted", "Image post created!")
        load_posts(win.children['!canvas'].children['!frame'])

def create_poll(username, win):
    question = simpledialog.askstring("New Poll", "Enter poll question:")
    if question:
        cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO posts (user_id, content) VALUES (%s, %s)", (user_id, f"[Poll]: {question}"))
        conn.commit()
        messagebox.showinfo("Posted", "Poll created!")
        load_posts(win.children['!canvas'].children['!frame'])
