import tkinter as tk
from tkinter import ttk
from login import LoginPage
from instagram_dashboard import InstagramDashboard

class CollegeBuzzApp:
    def __init__(self):
        # Initialize main window
        self.root = tk.Tk()
        self.root.state('zoomed')  # Start maximized on Windows
        self.root.configure(bg='#f0f2f5')
        
        # Set minimum window size
        self.root.minsize(1200, 800)
        
        # Configure styles for buttons, labels, etc.
        self.setup_styles()
        
        self.current_user = None
        self.current_page = None
        
        # Start with login page
        self.show_login()
    
    def setup_styles(self):
        """Configure modern styles for the application"""
        style = ttk.Style()
        
        # Modern button styles
        style.configure(
            'Modern.TButton',
            font=('Segoe UI', 10, 'bold'),
            padding=(15, 10),
            relief='flat'
        )
        
        style.configure(
            'Primary.TButton',
            background='#1877f2',
            foreground='white',
            font=('Segoe UI', 10, 'bold'),
            padding=(20, 12),
            relief='flat'
        )
        
        style.configure(
            'Success.TButton',
            background='#28a745',
            foreground='white',
            font=('Segoe UI', 10, 'bold'),
            padding=(20, 12),
            relief='flat'
        )
        
        style.configure(
            'Danger.TButton',
            background='#dc3545',
            foreground='white',
            font=('Segoe UI', 10, 'bold'),
            padding=(15, 8),
            relief='flat'
        )
    
    def show_login(self):
        """Display the login page"""
        # Clear current page
        if self.current_page:
            self.current_page.destroy()
        
        self.current_user = None
        self.current_page = LoginPage(self.root, self)
    
    def show_dashboard(self):
        """Display the main dashboard page"""
        if self.current_user:
            if self.current_page:
                self.current_page.destroy()
            self.current_page = InstagramDashboard(self.root, self)
        else:
            self.show_login()
    
    def run(self):
        """Run the main Tkinter event loop"""
        # Center the window on the screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

# Entry point
if __name__ == "__main__":
    app = CollegeBuzzApp()
    app.run()
