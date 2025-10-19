import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from datetime import datetime


class InstagramDashboard:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.db = DatabaseManager()
        self.posts = []
        self.image_path = None
        self.setup_instagram_ui()
        self.load_posts()
        
    def setup_instagram_ui(self):
        """Create Instagram-like UI"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("College Social Media - Feed")
        self.root.configure(bg='#fafafa')
        
        # Create main container
        self.main_container = tk.Frame(self.root, bg='#fafafa')
        self.main_container.pack(fill='both', expand=True)
        
        # Create Instagram-like header
        self.create_instagram_header()
        
        # Create main content area
        self.create_main_content()
        
    def create_instagram_header(self):
        """Create Instagram-like header"""
        # Header with Instagram styling
        header_frame = tk.Frame(self.main_container, bg='white', height=60)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Add border
        border_frame = tk.Frame(self.main_container, bg='#dbdbdb', height=1)
        border_frame.pack(fill='x')
        
        # Header content
        header_content = tk.Frame(header_frame, bg='white')
        header_content.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header_content, bg='white')
        left_frame.pack(side='left')
        
        # Instagram-like logo
        logo_label = tk.Label(
            left_frame,
            text="📱",
            font=("Segoe UI", 24),
            bg='white'
        )
        logo_label.pack(side='left', padx=(0, 10))
        
        # App title
        title_label = tk.Label(
            left_frame,
            text="College Social",
            font=("Segoe UI", 24, "bold"),
            fg='#262626',
            bg='white'
        )
        title_label.pack(side='left')
        
        # Center - Search bar
        center_frame = tk.Frame(header_content, bg='white')
        center_frame.pack(side='left', fill='x', expand=True, padx=50)
        
        # Search container
        search_container = tk.Frame(center_frame, bg='#f0f0f0', relief='solid', bd=1)
        search_container.pack(fill='x', pady=5)
        
        self.search_entry = tk.Entry(
            search_container,
            font=("Segoe UI", 12),
            relief='flat',
            bd=0,
            bg='#f0f0f0',
            fg='#8e8e8e',
            insertbackground='#262626'
        )
        self.search_entry.pack(fill='x', padx=15, pady=8)
        self.search_entry.insert(0, "Search...")
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)
        
        # Right side - Navigation and user
        right_frame = tk.Frame(header_content, bg='white')
        right_frame.pack(side='right')
        
        # Navigation icons
        nav_frame = tk.Frame(right_frame, bg='white')
        nav_frame.pack(side='left', padx=(0, 20))
        
        # Home button
        home_btn = tk.Button(
            nav_frame,
            text="🏠",
            command=self.show_home,
            bg='white',
            fg='#262626',
            font=("Segoe UI", 18),
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            activebackground='#f0f0f0'
        )
        home_btn.pack(side='left', padx=(0, 10))
        
        # Create post button
        create_btn = tk.Button(
            nav_frame,
            text="➕",
            command=self.show_create_post,
            bg='white',
            fg='#262626',
            font=("Segoe UI", 18),
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            activebackground='#f0f0f0'
        )
        create_btn.pack(side='left', padx=(0, 10))
        
        # Profile button
        profile_btn = tk.Button(
            nav_frame,
            text="👤",
            command=self.show_profile,
            bg='white',
            fg='#262626',
            font=("Segoe UI", 18),
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            activebackground='#f0f0f0'
        )
        profile_btn.pack(side='left', padx=(0, 10))
        
        # Logout button
        logout_btn = tk.Button(
            right_frame,
            text="Logout",
            command=self.logout,
            bg='#ed4956',
            fg='white',
            font=("Segoe UI", 11, "bold"),
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            activebackground='#dc3545'
        )
        logout_btn.pack(side='right')
        
    def create_main_content(self):
        """Create the main content area with Instagram-like layout"""
        # Main content container
        content_container = tk.Frame(self.main_container, bg='#fafafa')
        content_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create post section
        self.create_post_section(content_container)
        
        # Create posts feed
        self.create_posts_feed(content_container)
        
    def create_post_section(self, parent):
        """Create the post creation section"""
        # Post creation card
        post_card = tk.Frame(parent, bg='white', relief='solid', bd=1)
        post_card.pack(fill='x', pady=(0, 20))
        
        # Post header
        header_frame = tk.Frame(post_card, bg='white')
        header_frame.pack(fill='x', padx=20, pady=(20, 15))
        
        # User info
        user_info = tk.Frame(header_frame, bg='white')
        user_info.pack(side='left')
        
        # User avatar
        avatar_label = tk.Label(
            user_info,
            text="👤",
            font=("Segoe UI", 20),
            bg='white'
        )
        avatar_label.pack(side='left', padx=(0, 10))
        
        # User name
        user_label = tk.Label(
            user_info,
            text=f"@{self.app.current_user['username']}",
            font=("Segoe UI", 14, "bold"),
            fg='#262626',
            bg='white'
        )
        user_label.pack(side='left')
        
        # Post content area
        content_frame = tk.Frame(post_card, bg='white')
        content_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Post text area
        self.post_entry = tk.Text(
            content_frame,
            height=4,
            font=("Segoe UI", 14),
            relief='flat',
            bd=0,
            wrap='word',
            bg='white',
            fg='#262626',
            insertbackground='#262626',
            padx=0,
            pady=10
        )
        self.post_entry.pack(fill='x', pady=(0, 15))
        self.post_entry.insert('1.0', "What's on your mind?")
        self.post_entry.configure(fg='#8e8e8e')
        self.post_entry.bind('<FocusIn>', self.on_post_focus_in)
        self.post_entry.bind('<FocusOut>', self.on_post_focus_out)
        
        # Action buttons
        actions_frame = tk.Frame(content_frame, bg='white')
        actions_frame.pack(fill='x')
        
        # Left side - Media buttons
        left_actions = tk.Frame(actions_frame, bg='white')
        left_actions.pack(side='left')
        
        # Image button
        image_btn = tk.Button(
            left_actions,
            text="📷 Photo",
            command=self.upload_image,
            bg='white',
            fg='#0095f6',
            font=("Segoe UI", 12, "bold"),
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            activebackground='#f0f0f0'
        )
        image_btn.pack(side='left', padx=(0, 10))
        
        # Emoji button
        emoji_btn = tk.Button(
            left_actions,
            text="😊 Emoji",
            command=self.show_emoji_picker,
            bg='white',
            fg='#0095f6',
            font=("Segoe UI", 12, "bold"),
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            activebackground='#f0f0f0'
        )
        emoji_btn.pack(side='left')
        
        # Right side - Post button
        right_actions = tk.Frame(actions_frame, bg='white')
        right_actions.pack(side='right')
        
        # Image preview
        self.image_preview_label = tk.Label(
            right_actions,
            text="",
            bg='white',
            fg='#0095f6',
            font=("Segoe UI", 11, "bold")
        )
        self.image_preview_label.pack(side='right', padx=(0, 15))
        
        # Post button
        self.post_btn = tk.Button(
            right_actions,
            text="Share",
            command=self.save_post,
            bg='#0095f6',
            fg='white',
            font=("Segoe UI", 12, "bold"),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            activebackground='#1877f2'
        )
        self.post_btn.pack(side='right')
        
    def create_posts_feed(self, parent):
        """Create the posts feed section"""
        # Feed header
        feed_header = tk.Frame(parent, bg='#fafafa')
        feed_header.pack(fill='x', pady=(0, 15))
        
        # Feed title
        feed_title = tk.Label(
            feed_header,
            text="📰 Your Feed",
            font=("Segoe UI", 18, "bold"),
            fg='#262626',
            bg='#fafafa'
        )
        feed_title.pack(side='left')
        
        # Posts container with scrollbar
        posts_container = tk.Frame(parent, bg='#fafafa')
        posts_container.pack(fill='both', expand=True)
        
        # Create canvas and scrollbar
        self.posts_canvas = tk.Canvas(posts_container, bg='#fafafa', highlightthickness=0)
        self.scrollbar = tk.Scrollbar(posts_container, orient="vertical", command=self.posts_canvas.yview)
        self.scrollable_frame = tk.Frame(self.posts_canvas, bg='#fafafa')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.posts_canvas.configure(scrollregion=self.posts_canvas.bbox("all"))
        )
        
        self.posts_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.posts_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.posts_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            self.posts_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.posts_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def on_search_focus_in(self, event):
        """Handle search focus in"""
        if self.search_entry.get() == "Search...":
            self.search_entry.delete(0, 'end')
            self.search_entry.configure(fg='#262626')
            
    def on_search_focus_out(self, event):
        """Handle search focus out"""
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, "Search...")
            self.search_entry.configure(fg='#8e8e8e')
            
    def on_post_focus_in(self, event):
        """Handle post focus in"""
        if self.post_entry.get('1.0', 'end-1c') == "What's on your mind?":
            self.post_entry.delete('1.0', 'end')
            self.post_entry.configure(fg='#262626')
            
    def on_post_focus_out(self, event):
        """Handle post focus out"""
        if not self.post_entry.get('1.0', 'end-1c').strip():
            self.post_entry.insert('1.0', "What's on your mind?")
            self.post_entry.configure(fg='#8e8e8e')
            
    def upload_image(self):
        """Handle image upload"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
        )
        if file_path:
            self.image_path = file_path
            filename = os.path.basename(file_path)
            self.image_preview_label.config(text=f"📷 {filename}")
            
    def show_emoji_picker(self):
        """Show emoji picker dialog"""
        emoji_window = tk.Toplevel(self.root)
        emoji_window.title("Emoji Picker")
        emoji_window.geometry("300x200")
        emoji_window.configure(bg='white')
        emoji_window.resizable(False, False)
        emoji_window.transient(self.root)
        emoji_window.grab_set()
        
        # Emoji picker content
        tk.Label(
            emoji_window,
            text="😊 Choose an Emoji",
            font=("Segoe UI", 16, "bold"),
            fg='#0095f6',
            bg='white'
        ).pack(pady=(20, 15))
        
        # Emoji grid
        emoji_frame = tk.Frame(emoji_window, bg='white')
        emoji_frame.pack(fill='both', expand=True, padx=20)
        
        emojis = ["😊", "😂", "❤️", "👍", "🎉", "🔥", "💯", "✨", "🌟", "🎓"]
        
        for i, emoji in enumerate(emojis):
            btn = tk.Button(
                emoji_frame,
                text=emoji,
                command=lambda e=emoji: self.insert_emoji(e, emoji_window),
                bg='white',
                font=("Segoe UI", 16),
                relief='flat',
                padx=10,
                pady=5,
                cursor='hand2'
            )
            btn.grid(row=i//5, column=i%5, padx=5, pady=5)
            
    def insert_emoji(self, emoji, window):
        """Insert emoji into post"""
        current_text = self.post_entry.get('1.0', 'end-1c')
        if current_text == "What's on your mind?":
            self.post_entry.delete('1.0', 'end')
            self.post_entry.configure(fg='#262626')
        
        self.post_entry.insert(tk.INSERT, emoji)
        window.destroy()
        
    def save_post(self):
        """Save post"""
        content = self.post_entry.get("1.0", "end-1c").strip()
        
        if not content or content == "What's on your mind?":
            messagebox.showwarning("Empty Post", "Please write something before posting.")
            return
        
        # Show loading state
        self.post_btn.config(text="Posting...", state='disabled')
        self.root.update()
        
        try:
            # Save post
            post_id = self.db.create_post(self.app.current_user['id'], content, self.image_path)
            
            if post_id:
                messagebox.showinfo("Success", "🎉 Post published successfully!")
                
                # Clear form
                self.clear_form()
                
                # Reload posts
                self.load_posts()
            else:
                messagebox.showerror("Error", "Failed to save post.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save post: {str(e)}")
        finally:
            self.post_btn.config(text="Share", state='normal')
    
    def clear_form(self):
        """Clear all form fields"""
        self.post_entry.delete('1.0', 'end')
        self.post_entry.insert('1.0', "What's on your mind?")
        self.post_entry.configure(fg='#8e8e8e')
        self.image_path = None
        self.image_preview_label.config(text="")
    
    def load_posts(self):
        """Load and display posts"""
        # Clear existing posts
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get posts from database
        posts = self.db.get_posts()
        
        if not posts:
            # Show no posts message
            no_posts_label = tk.Label(
                self.scrollable_frame,
                text="No posts yet. Be the first to post!",
                font=("Segoe UI", 14),
                fg='#8e8e8e',
                bg='#fafafa'
            )
            no_posts_label.pack(pady=50)
            return
        
        # Display posts
        for post in posts:
            self.create_post_widget(post)
    
    def create_post_widget(self, post):
        """Create an Instagram-like post widget"""
        # Main post card
        post_card = tk.Frame(self.scrollable_frame, bg='white', relief='solid', bd=1)
        post_card.pack(fill='x', pady=(0, 20))
        
        # Post header
        header_frame = tk.Frame(post_card, bg='white')
        header_frame.pack(fill='x', padx=20, pady=(20, 15))
        
        # Left side - User info
        user_info = tk.Frame(header_frame, bg='white')
        user_info.pack(side='left')
        
        # User avatar
        avatar_label = tk.Label(
            user_info,
            text="👤",
            font=("Segoe UI", 20),
            bg='white'
        )
        avatar_label.pack(side='left', padx=(0, 10))
        
        # User name and info
        user_label = tk.Label(
            user_info,
            text=f"@{post['username']}",
            font=("Segoe UI", 14, "bold"),
            fg='#262626',
            bg='white'
        )
        user_label.pack(side='left')
        
        # Right side - More options
        options_btn = tk.Button(
            header_frame,
            text="⋯",
            command=lambda p=post: self.show_post_options(p),
            bg='white',
            fg='#262626',
            font=("Segoe UI", 16),
            relief='flat',
            padx=5,
            pady=2,
            cursor='hand2',
            activebackground='#f0f0f0'
        )
        options_btn.pack(side='right')
        
        # Post content
        content_frame = tk.Frame(post_card, bg='white')
        content_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # Content text
        content_label = tk.Label(
            content_frame,
            text=post['content'],
            font=("Segoe UI", 14),
            fg='#262626',
            bg='white',
            wraplength=600,
            justify='left'
        )
        content_label.pack(anchor='w')
        
        # Image if exists
        if post['image_path'] and os.path.exists(post['image_path']):
            try:
                img = Image.open(post['image_path'])
                img.thumbnail((600, 600))
                photo = ImageTk.PhotoImage(img)
                
                img_label = tk.Label(content_frame, image=photo, bg='white')
                img_label.image = photo  # Keep a reference
                img_label.pack(pady=(15, 0))
            except Exception as e:
                print(f"Error loading image: {e}")
        
        # Post footer with engagement
        footer_frame = tk.Frame(post_card, bg='white')
        footer_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Engagement buttons
        engagement_frame = tk.Frame(footer_frame, bg='white')
        engagement_frame.pack(fill='x')
        
        # Like button
        like_btn = tk.Button(
            engagement_frame,
            text="❤️",
            command=lambda p=post: self.toggle_like(p),
            bg='white',
            fg='#262626',
            font=("Segoe UI", 16),
            relief='flat',
            padx=5,
            pady=5,
            cursor='hand2',
            activebackground='#f0f0f0'
        )
        like_btn.pack(side='left', padx=(0, 15))
        
        # Comment button
        comment_btn = tk.Button(
            engagement_frame,
            text="💬",
            command=lambda p=post: self.show_comments(p),
            bg='white',
            fg='#262626',
            font=("Segoe UI", 16),
            relief='flat',
            padx=5,
            pady=5,
            cursor='hand2',
            activebackground='#f0f0f0'
        )
        comment_btn.pack(side='left', padx=(0, 15))
        
        # Share button
        share_btn = tk.Button(
            engagement_frame,
            text="📤",
            command=lambda p=post: self.share_post(p),
            bg='white',
            fg='#262626',
            font=("Segoe UI", 16),
            relief='flat',
            padx=5,
            pady=5,
            cursor='hand2',
            activebackground='#f0f0f0'
        )
        share_btn.pack(side='left')
        
        # Like count
        like_count_label = tk.Label(
            footer_frame,
            text=f"{post['like_count']} likes",
            font=("Segoe UI", 12, "bold"),
            fg='#262626',
            bg='white'
        )
        like_count_label.pack(anchor='w', pady=(10, 5))
        
        # Timestamp
        time_label = tk.Label(
            footer_frame,
            text=post['created_at'].strftime("%b %d, %Y at %I:%M %p"),
            font=("Segoe UI", 10),
            fg='#8e8e8e',
            bg='white'
        )
        time_label.pack(anchor='w')
        
    def toggle_like(self, post):
        """Toggle like on a post"""
        action = self.db.like_post(self.app.current_user['id'], post['id'])
        if action:
            self.load_posts()  # Refresh to show updated like count
            
    def show_comments(self, post):
        """Show comments dialog"""
        comments_window = tk.Toplevel(self.root)
        comments_window.title("Comments")
        comments_window.geometry("500x400")
        comments_window.configure(bg='white')
        comments_window.transient(self.root)
        comments_window.grab_set()
        
        # Comments header
        header_frame = tk.Frame(comments_window, bg='white')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        tk.Label(
            header_frame,
            text=f"Comments on @{post['username']}'s post",
            font=("Segoe UI", 14, "bold"),
            fg='#262626',
            bg='white'
        ).pack()
        
        # Comments list
        comments_frame = tk.Frame(comments_window, bg='white')
        comments_frame.pack(fill='both', expand=True, padx=20)
        
        # Get comments
        comments = self.db.get_comments(post['id'])
        
        if comments:
            for comment in comments:
                comment_frame = tk.Frame(comments_frame, bg='#f8f9fa', relief='solid', bd=1)
                comment_frame.pack(fill='x', pady=5)
                
                tk.Label(
                    comment_frame,
                    text=f"@{comment['username']}: {comment['content']}",
                    font=("Segoe UI", 12),
                    fg='#262626',
                    bg='#f8f9fa',
                    wraplength=400,
                    justify='left'
                ).pack(anchor='w', padx=10, pady=5)
        else:
            tk.Label(
                comments_frame,
                text="No comments yet. Be the first to comment!",
                font=("Segoe UI", 12),
                fg='#8e8e8e',
                bg='white'
            ).pack(pady=20)
        
        # Add comment section
        add_comment_frame = tk.Frame(comments_window, bg='white')
        add_comment_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        comment_entry = tk.Entry(
            add_comment_frame,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        comment_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        def add_comment():
            content = comment_entry.get().strip()
            if content:
                if self.db.add_comment(self.app.current_user['id'], post['id'], content):
                    messagebox.showinfo("Success", "Comment added!")
                    comments_window.destroy()
                    self.show_comments(post)  # Refresh comments
                else:
                    messagebox.showerror("Error", "Failed to add comment.")
        
        tk.Button(
            add_comment_frame,
            text="Post",
            command=add_comment,
            bg='#0095f6',
            fg='white',
            font=("Segoe UI", 11, "bold"),
            relief='flat',
            padx=15,
            pady=5
        ).pack(side='right')
        
    def share_post(self, post):
        """Share a post"""
        messagebox.showinfo("Share", f"Shared @{post['username']}'s post!")
        
    def show_post_options(self, post):
        """Show post options menu"""
        options_window = tk.Toplevel(self.root)
        options_window.title("Post Options")
        options_window.geometry("200x150")
        options_window.configure(bg='white')
        options_window.transient(self.root)
        options_window.grab_set()
        
        # Options
        tk.Button(
            options_window,
            text="Report",
            command=lambda: messagebox.showinfo("Report", "Post reported!"),
            bg='white',
            fg='#ed4956',
            font=("Segoe UI", 12),
            relief='flat',
            padx=20,
            pady=10
        ).pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            options_window,
            text="Copy Link",
            command=lambda: messagebox.showinfo("Copy", "Link copied to clipboard!"),
            bg='white',
            fg='#262626',
            font=("Segoe UI", 12),
            relief='flat',
            padx=20,
            pady=10
        ).pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            options_window,
            text="Close",
            command=options_window.destroy,
            bg='white',
            fg='#8e8e8e',
            font=("Segoe UI", 12),
            relief='flat',
            padx=20,
            pady=10
        ).pack(fill='x', padx=10, pady=5)
        
    def show_home(self):
        """Show home view"""
        pass
        
    def show_create_post(self):
        """Show create post view"""
        pass
        
    def show_profile(self):
        """Show profile view"""
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Profile")
        profile_window.geometry("400x500")
        profile_window.configure(bg='white')
        profile_window.transient(self.root)
        profile_window.grab_set()
        
        # Profile content
        tk.Label(
            profile_window,
            text="👤",
            font=("Segoe UI", 48),
            bg='white'
        ).pack(pady=(30, 10))
        
        tk.Label(
            profile_window,
            text=f"@{self.app.current_user['username']}",
            font=("Segoe UI", 20, "bold"),
            fg='#262626',
            bg='white'
        ).pack(pady=(0, 5))
        
        tk.Label(
            profile_window,
            text=self.app.current_user['full_name'],
            font=("Segoe UI", 16),
            fg='#8e8e8e',
            bg='white'
        ).pack(pady=(0, 20))
        
        # Profile stats
        stats_frame = tk.Frame(profile_window, bg='white')
        stats_frame.pack(fill='x', padx=50, pady=20)
        
        tk.Label(stats_frame, text="Posts", font=("Segoe UI", 14, "bold"), bg='white').pack(side='left', padx=20)
        tk.Label(stats_frame, text="Followers", font=("Segoe UI", 14, "bold"), bg='white').pack(side='left', padx=20)
        tk.Label(stats_frame, text="Following", font=("Segoe UI", 14, "bold"), bg='white').pack(side='left', padx=20)
        
    def logout(self):
        """Handle logout"""
        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            icon='question'
        )
        if result:
            self.app.show_login()
