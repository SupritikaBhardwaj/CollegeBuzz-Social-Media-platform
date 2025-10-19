import tkinter as tk
from tkinter import messagebox, ttk
from social_database import SocialDatabase

class InstagramLogin:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.db = SocialDatabase()
        self.setup_login_ui()
        
    def setup_login_ui(self):
        """Create the Instagram-like login page UI"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("College Social Media - Login")
        self.root.configure(bg='#fafafa')
        
        # Create main container
        self.main_container = tk.Frame(self.root, bg='#fafafa')
        self.main_container.pack(fill='both', expand=True)
        
        # Create the login card
        self.create_login_card()
        
    def create_login_card(self):
        """Create the main login card with Instagram-like design"""
        # Main login card container
        card_container = tk.Frame(self.main_container, bg='#fafafa')
        card_container.place(relx=0.5, rely=0.5, anchor='center', width=350, height=500)
        
        # Login card with Instagram-like styling
        login_card = tk.Frame(card_container, bg='white', relief='solid', bd=1)
        login_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add some padding inside the card
        card_content = tk.Frame(login_card, bg='white')
        card_content.pack(fill='both', expand=True, padx=40, pady=40)
        
        # App logo and title
        self.create_header(card_content)
        
        # Login form
        self.create_login_form(card_content)
        
        # Footer with sign up option
        self.create_footer(card_content)
        
    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg='white')
        header_frame.pack(fill='x', pady=(0, 30))
        
        # App logo
        logo_label = tk.Label(
            header_frame,
            text="📱",
            font=("Segoe UI", 48),
            bg='white'
        )
        logo_label.pack()
        
        # App title
        title_label = tk.Label(
            header_frame,
            text="College Social",
            font=("Segoe UI", 28, "bold"),
            fg='#262626',
            bg='white'
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Connect with your college community",
            font=("Segoe UI", 14),
            fg='#8e8e8e',
            bg='white'
        )
        subtitle_label.pack()
        
    def create_login_form(self, parent):
        """Create the login form"""
        form_frame = tk.Frame(parent, bg='white')
        form_frame.pack(fill='x', pady=(0, 20))
        
        # Username field
        username_frame = tk.Frame(form_frame, bg='white')
        username_frame.pack(fill='x', pady=(0, 15))
        
        self.username_entry = tk.Entry(
            username_frame,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            bg='#fafafa',
            fg='#262626',
            insertbackground='#0095f6'
        )
        self.username_entry.pack(fill='x', pady=(0, 5))
        self.username_entry.insert(0, "Username")
        self.username_entry.bind('<FocusIn>', self.on_username_focus_in)
        self.username_entry.bind('<FocusOut>', self.on_username_focus_out)
        
        # Password field
        password_frame = tk.Frame(form_frame, bg='white')
        password_frame.pack(fill='x', pady=(0, 20))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            bg='#fafafa',
            fg='#262626',
            show='*',
            insertbackground='#0095f6'
        )
        self.password_entry.pack(fill='x', pady=(0, 5))
        self.password_entry.insert(0, "Password")
        self.password_entry.bind('<FocusIn>', self.on_password_focus_in)
        self.password_entry.bind('<FocusOut>', self.on_password_focus_out)
        
        # Login button
        self.login_btn = tk.Button(
            form_frame,
            text="Log In",
            command=self.login,
            bg='#0095f6',
            fg='white',
            font=("Segoe UI", 14, "bold"),
            relief='flat',
            padx=20,
            pady=12,
            cursor='hand2',
            activebackground='#1877f2',
            activeforeground='white'
        )
        self.login_btn.pack(fill='x', pady=(0, 15))
        
        # Demo credentials
        demo_frame = tk.Frame(form_frame, bg='#fafafa', relief='solid', bd=1)
        demo_frame.pack(fill='x', pady=(0, 15))
        
        demo_label = tk.Label(
            demo_frame,
            text="💡 Demo: john_doe / password123",
            font=("Segoe UI", 10),
            fg='#8e8e8e',
            bg='#fafafa'
        )
        demo_label.pack(pady=8)
        
    def create_footer(self, parent):
        """Create the footer section"""
        footer_frame = tk.Frame(parent, bg='white')
        footer_frame.pack(fill='x', pady=(20, 0))
        
        # Divider
        divider = tk.Frame(footer_frame, bg='#dbdbdb', height=1)
        divider.pack(fill='x', pady=(0, 20))
        
        # Sign up section
        signup_frame = tk.Frame(footer_frame, bg='white')
        signup_frame.pack()
        
        signup_text = tk.Label(
            signup_frame,
            text="Don't have an account?",
            font=("Segoe UI", 12),
            fg='#262626',
            bg='white'
        )
        signup_text.pack(side='left')
        
        signup_link = tk.Button(
            signup_frame,
            text="Sign Up",
            command=self.show_signup,
            bg='white',
            fg='#0095f6',
            font=("Segoe UI", 12, "bold"),
            relief='flat',
            cursor='hand2',
            activebackground='white',
            activeforeground='#1877f2'
        )
        signup_link.pack(side='left', padx=(5, 0))
        
    def on_username_focus_in(self, event):
        """Handle username focus in"""
        if self.username_entry.get() == "Username":
            self.username_entry.delete(0, 'end')
            self.username_entry.configure(fg='#262626')
            
    def on_username_focus_out(self, event):
        """Handle username focus out"""
        if not self.username_entry.get().strip():
            self.username_entry.insert(0, "Username")
            self.username_entry.configure(fg='#8e8e8e')
            
    def on_password_focus_in(self, event):
        """Handle password focus in"""
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, 'end')
            self.password_entry.configure(fg='#262626', show='*')
            
    def on_password_focus_out(self, event):
        """Handle password focus out"""
        if not self.password_entry.get().strip():
            self.password_entry.insert(0, "Password")
            self.password_entry.configure(fg='#8e8e8e', show='')
            
    def login(self):
        """Handle login authentication"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if username == "Username" or password == "Password":
            messagebox.showwarning("Login Error", "Please enter your credentials.")
            return
            
        if not username or not password:
            messagebox.showwarning("Login Error", "Please enter both username and password.")
            return
            
        # Authenticate user
        user_data = self.db.authenticate_user(username, password)
        
        if user_data:
            self.app.current_user = user_data
            self.app.show_main_app()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")
    
    def show_signup(self):
        """Show signup dialog"""
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("400x600")
        signup_window.configure(bg='white')
        signup_window.resizable(False, False)
        signup_window.transient(self.root)
        signup_window.grab_set()
        
        # Signup form
        tk.Label(
            signup_window,
            text="📱 College Social",
            font=("Segoe UI", 24, "bold"),
            fg='#262626',
            bg='white'
        ).pack(pady=(30, 10))
        
        tk.Label(
            signup_window,
            text="Sign up to see photos and videos from your college",
            font=("Segoe UI", 12),
            fg='#8e8e8e',
            bg='white'
        ).pack(pady=(0, 30))
        
        # Form fields
        fields_frame = tk.Frame(signup_window, bg='white')
        fields_frame.pack(fill='x', padx=40)
        
        # Username
        username_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            bg='#fafafa',
            fg='#262626'
        )
        username_entry.pack(fill='x', pady=(0, 15))
        username_entry.insert(0, "Username")
        
        # Email
        email_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            bg='#fafafa',
            fg='#262626'
        )
        email_entry.pack(fill='x', pady=(0, 15))
        email_entry.insert(0, "Email")
        
        # Full Name
        fullname_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            bg='#fafafa',
            fg='#262626'
        )
        fullname_entry.pack(fill='x', pady=(0, 15))
        fullname_entry.insert(0, "Full Name")
        
        # Password
        password_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            bg='#fafafa',
            fg='#262626',
            show='*'
        )
        password_entry.pack(fill='x', pady=(0, 20))
        password_entry.insert(0, "Password")
        
        def signup():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            full_name = fullname_entry.get().strip()
            password = password_entry.get().strip()
            
            if not all([username, email, full_name, password]):
                messagebox.showwarning("Signup Error", "Please fill all fields.")
                return
                
            if self.db.create_user(username, email, password, full_name):
                messagebox.showinfo("Success", "Account created successfully!")
                signup_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to create account.")
        
        # Sign up button
        tk.Button(
            signup_window,
            text="Sign Up",
            command=signup,
            bg='#0095f6',
            fg='white',
            font=("Segoe UI", 14, "bold"),
            relief='flat',
            padx=20,
            pady=12
        ).pack(fill='x', padx=40, pady=20)
