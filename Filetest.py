import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import random
import datetime
import json
import threading
import time

class AdvancedChatBot:
    def __init__(self):
        self.setup_window()
        self.setup_bot_personality()
        self.setup_widgets()
        self.chat_history = []
        
    def setup_window(self):
        """Initialize the main window with modern styling"""
        self.root = tk.Tk()
        self.root.title("🤖 Advanced ChatBot v2.0")
        self.root.geometry("700x800")
        self.root.configure(bg='#0d1117')
        self.root.resizable(True, True)
        
        # Set window icon (optional)
        try:
            self.root.iconbitmap('chatbot.ico')
        except:
            pass
    
    def setup_bot_personality(self):
        """Define bot responses and personality"""
        self.responses = {
            'greetings': [
                "Hello there! 👋 How can I brighten your day?",
                "Hey! Great to see you! What's on your mind?",
                "Hi! I'm here and ready to chat! 😊",
                "Greetings, human! Let's have an awesome conversation!"
            ],
            'jokes': [
                "Why don't scientists trust atoms? Because they make up everything! 😄",
                "I told my computer I needed a break, and now it won't stop sending me Kit-Kat ads! 🍫",
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "I would tell you a joke about UDP, but you might not get it... 📡",
                "Why was the math book sad? It had too many problems! 📚"
            ],
            'wisdom': [
                "The best time to plant a tree was 20 years ago. The second best time is now. 🌳",
                "Don't watch the clock; do what it does. Keep going. ⏰",
                "Life is like riding a bicycle. To keep your balance, you must keep moving. 🚴",
                "The only way to do great work is to love what you do. 💝"
            ],
            'compliments': [
                "You're absolutely amazing! ⭐",
                "I think you're pretty awesome! 🌟",
                "You have great taste in chatbots! 😉",
                "You're the kind of person who makes the world brighter! ☀️"
            ],
            'default': [
                "That's interesting! Tell me more! 🤔",
                "Hmm, I'm processing that... What else is on your mind? 🧠",
                "I love our conversations! Keep them coming! 💬",
                "You know what? You're pretty cool! What else can we chat about? 😎"
            ]
        }
        
        self.keywords = {
            'greetings': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
            'jokes': ['joke', 'funny', 'laugh', 'humor', 'comedy', 'fun'],
            'wisdom': ['advice', 'wisdom', 'quote', 'inspiration', 'motivate', 'help'],
            'compliments': ['compliment', 'praise', 'nice', 'good job', 'awesome', 'amazing']
        }
    
    def setup_widgets(self):
        """Create and configure all GUI widgets"""
        # Header frame
        header_frame = tk.Frame(self.root, bg='#21262d', height=60)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Title label with emoji
        title_label = tk.Label(
            header_frame, 
            text="🤖 Advanced ChatBot", 
            font=('Segoe UI', 18, 'bold'),
            bg='#21262d', 
            fg='#58a6ff'
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Status label
        self.status_label = tk.Label(
            header_frame, 
            text="● Online", 
            font=('Segoe UI', 10),
            bg='#21262d', 
            fg='#3fb950'
        )
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Chat display frame
        chat_frame = tk.Frame(self.root, bg='#0d1117')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat window with custom styling
        self.chat_window = scrolledtext.ScrolledText(
            chat_frame,
            state=tk.DISABLED,
            wrap=tk.WORD,
            bg='#161b22',
            fg='#c9d1d9',
            font=('Consolas', 11),
            insertbackground='#58a6ff',
            selectbackground='#264f78',
            relief=tk.FLAT,
            bd=0
        )
        self.chat_window.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for different message types
        self.chat_window.tag_configure("user", foreground="#58a6ff", font=('Consolas', 11, 'bold'))
        self.chat_window.tag_configure("bot", foreground="#3fb950", font=('Consolas', 11, 'bold'))
        self.chat_window.tag_configure("system", foreground="#f85149", font=('Consolas', 9, 'italic'))
        self.chat_window.tag_configure("timestamp", foreground="#8b949e", font=('Consolas', 8))
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#0d1117')
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # User input entry
        self.user_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 12),
            bg='#21262d',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            relief=tk.FLAT,
            bd=10
        )
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_entry.bind('<Return>', self.send_message)
        self.user_entry.bind('<KeyPress>', self.on_typing)
        
        # Send button with hover effects
        self.send_button = tk.Button(
            input_frame,
            text="Send 📤",
            font=('Segoe UI', 10, 'bold'),
            bg='#238636',
            fg='white',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            command=self.send_message,
            cursor='hand2'
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Bind hover effects
        self.send_button.bind('<Enter>', self.on_button_hover)
        self.send_button.bind('<Leave>', self.on_button_leave)
        
        # Menu bar
        self.create_menu()
        
        # Welcome message
        self.add_system_message("Welcome! I'm your advanced chatbot. Type anything to start chatting! 🚀")
        
        # Focus on entry
        self.user_entry.focus()
    
    def create_menu(self):
        """Create menu bar with additional options"""
        menubar = tk.Menu(self.root, bg='#21262d', fg='#c9d1d9')
        self.root.config(menu=menubar)
        
        # Chat menu
        chat_menu = tk.Menu(menubar, tearoff=0, bg='#21262d', fg='#c9d1d9')
        menubar.add_cascade(label="Chat", menu=chat_menu)
        chat_menu.add_command(label="Clear Chat", command=self.clear_chat)
        chat_menu.add_command(label="Save Chat", command=self.save_chat)
        chat_menu.add_separator()
        chat_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg='#21262d', fg='#c9d1d9')
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def on_button_hover(self, event):
        """Button hover effect"""
        self.send_button.config(bg='#2ea043')
    
    def on_button_leave(self, event):
        """Button leave effect"""
        self.send_button.config(bg='#238636')
    
    def on_typing(self, event):
        """Show typing indicator"""
        self.status_label.config(text="● Typing...", fg='#f85149')
        self.root.after(1000, lambda: self.status_label.config(text="● Online", fg='#3fb950'))
    
    def get_timestamp(self):
        """Get current timestamp"""
        return datetime.datetime.now().strftime("%H:%M")
    
    def add_message(self, sender, message, tag):
        """Add message to chat window with timestamp"""
        self.chat_window.config(state=tk.NORMAL)
        timestamp = self.get_timestamp()
        
        # Add timestamp
        self.chat_window.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add sender and message
        self.chat_window.insert(tk.END, f"{sender}: ", tag)
        self.chat_window.insert(tk.END, f"{message}\n\n")
        
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.yview(tk.END)
    
    def add_system_message(self, message):
        """Add system message"""
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"[SYSTEM] {message}\n\n", "system")
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.yview(tk.END)
    
    def get_bot_response(self, user_input):
        """Generate bot response based on user input"""
        user_input_lower = user_input.lower()
        
        # Check for keywords and respond accordingly
        for category, keywords in self.keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return random.choice(self.responses[category])
        
        # Special responses for specific inputs
        if 'time' in user_input_lower:
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')} ⏰"
        
        if 'date' in user_input_lower:
            return f"Today is {datetime.datetime.now().strftime('%B %d, %Y')} 📅"
        
        if 'weather' in user_input_lower:
            weather_responses = [
                "I wish I could check the weather for you! Try a weather app! ☀️",
                "It's always sunny in the digital world! 🌞",
                "I'm not connected to weather services, but I hope it's nice! 🌤️"
            ]
            return random.choice(weather_responses)
        
        if any(word in user_input_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
            return "Goodbye! It was great chatting with you! Come back soon! 👋"
        
        # Default response
        return random.choice(self.responses['default'])
    
    def send_message(self, event=None):
        """Send user message and get bot response"""
        user_text = self.user_entry.get().strip()
        if not user_text:
            return
        
        # Add user message
        self.add_message("You", user_text, "user")
        self.chat_history.append(("user", user_text))
        
        # Clear entry
        self.user_entry.delete(0, tk.END)
        
        # Show bot is thinking
        self.status_label.config(text="● Thinking...", fg='#f85149')
        
        # Simulate thinking delay
        self.root.after(1000, lambda: self.send_bot_response(user_text))
    
    def send_bot_response(self, user_text):
        """Send bot response after delay"""
        bot_response = self.get_bot_response(user_text)
        self.add_message("ChatBot", bot_response, "bot")
        self.chat_history.append(("bot", bot_response))
        
        # Reset status
        self.status_label.config(text="● Online", fg='#3fb950')
    
    def clear_chat(self):
        """Clear chat window"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat?"):
            self.chat_window.config(state=tk.NORMAL)
            self.chat_window.delete(1.0, tk.END)
            self.chat_window.config(state=tk.DISABLED)
            self.chat_history.clear()
            self.add_system_message("Chat cleared! Ready for a fresh conversation! 🧹")
    
    def save_chat(self):
        """Save chat history to file"""
        if not self.chat_history:
            messagebox.showinfo("Save Chat", "No chat history to save!")
            return
        
        try:
            filename = f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Save Chat", f"Chat saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save chat: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
🤖 Advanced ChatBot v2.0

A modern, feature-rich chatbot built with Python and Tkinter.

Features:
• Modern dark theme UI
• Intelligent response system
• Chat history saving
• Typing indicators
• Timestamps
• Emoji support
• Multiple conversation topics

Created with ❤️ using Python
        """
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the chatbot"""
        self.root.mainloop()

# Run the chatbot
if __name__ == "__main__":
    chatbot = AdvancedChatBot()
    chatbot.run()
