"""
Modern GUI Interface for the AI Agent
Built with Tkinter with modern styling and customization options
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import json
from pathlib import Path
from config import THEMES, DEFAULT_SETTINGS, FONT_SIZES, AVAILABLE_MODELS, WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from agent import AIAgent


class SettingsManager:
    """Manages user settings persistence"""
    
    def __init__(self, settings_file="settings.json"):
        self.settings_file = Path(__file__).parent / settings_file
        self.settings = self._load_settings()
    
    def _load_settings(self):
        """Load settings from file or use defaults"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                return DEFAULT_SETTINGS.copy()
        return DEFAULT_SETTINGS.copy()
    
    def save_settings(self, settings):
        """Save settings to file"""
        self.settings = settings
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default or DEFAULT_SETTINGS.get(key))
    
    def update(self, **kwargs):
        """Update multiple settings"""
        self.settings.update(kwargs)
        self.save_settings(self.settings)


class ModernGUI:
    """
    Modern AI Agent Interface
    Combines aesthetics with functionality
    """
    
    def __init__(self, root, agent):
        self.root = root
        self.agent = agent
        self.settings_manager = SettingsManager()
        
        # Current settings
        self.current_theme = self.settings_manager.get("theme", "dark")
        self.current_font_size = self.settings_manager.get("font_size", 11)
        self.current_font_family = self.settings_manager.get("font_family", "Segoe UI")
        
        # Get theme colors
        self.colors = THEMES[self.current_theme]
        
        # Configure window
        self.root.title("Mon Agent IA - Conversationnel")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.root.configure(bg=self.colors["bg_main"])
        
        # Track if settings panel is open
        self.settings_open = False
        
        self._create_interface()
        self._apply_theme()
        
        # Bind Enter key to send message
        self.entry.bind("<Return>", lambda e: self.send_message())
        self.entry.bind("<Shift-Return>", lambda e: self.entry.insert(tk.INSERT, "\n"))
    
    def _create_interface(self):
        """Create the main interface"""
        
        # ============ TOP BAR ============
        top_bar = tk.Frame(self.root, bg=self.colors["bg_secondary"], height=60)
        top_bar.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        top_bar.pack_propagate(False)
        
        # Title
        title = tk.Label(
            top_bar, 
            text="🤖 Agent IA Conversationnel",
            font=(self.current_font_family, self.current_font_size + 3, "bold"),
            bg=self.colors["bg_secondary"],
            fg=self.colors["accent"]
        )
        title.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Settings button
        settings_btn = tk.Button(
            top_bar,
            text="⚙️ Paramètres",
            command=self.toggle_settings,
            bg=self.colors["accent"],
            fg=self.colors["user_text"],
            font=(self.current_font_family, self.current_font_size - 1),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        settings_btn.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # ============ MAIN CONTENT AREA ============
        main_frame = tk.Frame(self.root, bg=self.colors["bg_main"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_main"],
            font=(self.current_font_family, self.current_font_size),
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            padx=10,
            pady=10
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_area.config(state=tk.DISABLED)
        
        # Configure chat area text tags
        self.chat_area.tag_config("user", foreground=self.colors["user_text"], font=(self.current_font_family, self.current_font_size, "bold"))
        self.chat_area.tag_config("agent", foreground=self.colors["agent_text"], font=(self.current_font_family, self.current_font_size))
                # Enable copy functionality for chat area
        self._enable_copy_paste(self.chat_area)
                # ============ INPUT AREA ============
        input_frame = tk.Frame(main_frame, bg=self.colors["bg_main"])
        input_frame.pack(fill=tk.X)
        
        # Message entry
        self.entry = tk.Entry(
            input_frame,
            font=(self.current_font_family, self.current_font_size),
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_main"],
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            insertbackground=self.colors["accent"]
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Activer le copier-coller pour l'entry
        self._enable_copy_paste(self.entry)
        
        # Send button - Charismatic design
        self.send_btn = tk.Button(
            input_frame,
            text="✉️  ENVOYER",
            command=self.send_message,
            bg=self.colors["accent"],
            fg=self.colors["user_text"],
            font=(self.current_font_family, self.current_font_size + 1, "bold"),
            relief=tk.FLAT,
            padx=25,
            pady=8,
            cursor="hand2",
            activebackground=self.colors["accent_hover"],
            activeforeground=self.colors["user_text"]
        )
        self.send_btn.pack(side=tk.RIGHT, padx=0)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Prêt à converser...",
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_secondary"],
            font=(self.current_font_family, self.current_font_size - 2),
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10)
    
    def send_message(self):
        """Send a message and get a response"""
        user_input = self.entry.get().strip()
        if not user_input:
            return
        
        # Display user message
        self._display_message("👤 Toi", user_input, "user")
        self.entry.delete(0, tk.END)
        self.send_btn.config(state=tk.DISABLED)
        self.status_bar.config(text="⏳ Agent réfléchit...")
        self.root.update()
        
        try:
            # Get AI response
            response = self.agent.send_message(user_input)
            self._display_message("🤖 Agent", response, "agent")
            self.status_bar.config(text=f"✅ Message envoyé | Conversation: {self.agent.get_conversation_length()} messages")
        
        except Exception as e:
            self._display_message("❌ Erreur", f"Erreur lors de l'appel API: {str(e)}", "agent")
            self.status_bar.config(text="❌ Erreur - vérifiez votre clé API")
        
        finally:
            self.send_btn.config(state=tk.NORMAL)
    
    def _display_message(self, speaker, message, tag):
        """Display a message in the chat area"""
        self.chat_area.config(state=tk.NORMAL)
        
        # Add speaker line
        self.chat_area.insert(tk.END, f"{speaker}:\n", tag)
        
        # Add message
        self.chat_area.insert(tk.END, f"{message}\n\n")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def toggle_settings(self):
        """Toggle settings panel"""
        if self.settings_open:
            self.close_settings()
        else:
            self.open_settings()
    
    def open_settings(self):
        """Open settings window"""
        self.settings_open = True
        
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Paramètres")
        settings_window.geometry("400x400")
        settings_window.configure(bg=self.colors["bg_main"])
        
        # ============ THEME SETTING ============
        tk.Label(
            settings_window,
            text="Thème",
            font=(self.current_font_family, self.current_font_size + 1, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["text_main"]
        ).pack(pady=(15, 5), padx=20, anchor=tk.W)
        
        theme_var = tk.StringVar(value=self.current_theme)
        for theme in THEMES.keys():
            tk.Radiobutton(
                settings_window,
                text=f"{'🌙' if theme == 'dark' else '☀️'} {theme.capitalize()}",
                variable=theme_var,
                value=theme,
                command=lambda t=theme: self.change_theme(t),
                bg=self.colors["bg_main"],
                fg=self.colors["text_main"],
                selectcolor=self.colors["bg_secondary"],
                font=(self.current_font_family, self.current_font_size)
            ).pack(padx=30, anchor=tk.W)
        
        # ============ FONT SIZE SETTING ============
        tk.Label(
            settings_window,
            text="Taille de police",
            font=(self.current_font_family, self.current_font_size + 1, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["text_main"]
        ).pack(pady=(15, 5), padx=20, anchor=tk.W)
        
        size_var = tk.StringVar(value=str(self.current_font_size))
        size_scale = tk.Scale(
            settings_window,
            from_=9,
            to=16,
            orient=tk.HORIZONTAL,
            variable=size_var,
            bg=self.colors["bg_secondary"],
            fg=self.colors["text_main"],
            command=lambda s: self.change_font_size(int(s))
        )
        size_scale.pack(padx=20, fill=tk.X)
        
        # ============ MODEL SETTING ============
        tk.Label(
            settings_window,
            text="Modèle IA",
            font=(self.current_font_family, self.current_font_size + 1, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["text_main"]
        ).pack(pady=(15, 5), padx=20, anchor=tk.W)
        
        model_var = tk.StringVar(value=self.agent.get_model())
        model_menu = ttk.Combobox(
            settings_window,
            textvariable=model_var,
            values=AVAILABLE_MODELS,
            state="readonly",
            width=30
        )
        model_menu.pack(padx=20, fill=tk.X)
        model_menu.bind("<<ComboboxSelected>>", lambda e: self.change_model(model_var.get()))
        
        # ============ BUTTONS ============
        button_frame = tk.Frame(settings_window, bg=self.colors["bg_main"])
        button_frame.pack(pady=20, fill=tk.X, padx=20)
        
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Effacer historique",
            command=self.clear_history,
            bg="#ff6b6b",
            fg="white",
            font=(self.current_font_family, self.current_font_size - 1),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        clear_btn.pack(pady=5, fill=tk.X)
        
        close_btn = tk.Button(
            button_frame,
            text="✓ Fermer",
            command=settings_window.destroy,
            bg=self.colors["accent"],
            fg=self.colors["user_text"],
            font=(self.current_font_family, self.current_font_size - 1),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        close_btn.pack(pady=5, fill=tk.X)
        
        settings_window.protocol("WM_DELETE_WINDOW", self.close_settings)
    
    def close_settings(self):
        """Close settings panel"""
        self.settings_open = False
    
    def change_theme(self, theme):
        """Change the application theme"""
        self.current_theme = theme
        self.colors = THEMES[theme]
        self.settings_manager.update(theme=theme)
        messagebox.showinfo("Thème", "Le thème sera appliqué au redémarrage de l'application.")
    
    def change_font_size(self, size):
        """Change the font size"""
        self.current_font_size = size
        self.settings_manager.update(font_size=size)
        messagebox.showinfo("Police", "La taille de police sera appliquée au redémarrage.")
    
    def change_model(self, model):
        """Change the AI model"""
        try:
            self.agent.set_model(model)
            self.status_bar.config(text=f"✅ Modèle changé en: {model}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de changer le modèle: {e}")
    
    def clear_history(self):
        """Clear conversation history"""
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir effacer l'historique?"):
            self.agent.clear_history()
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.delete(1.0, tk.END)
            self.chat_area.config(state=tk.DISABLED)
            self.status_bar.config(text="✅ Historique effacé")
    
    def _enable_copy_paste(self, widget):
        """Enable copy/paste functionality for Entry and Text widgets"""
        if isinstance(widget, tk.Entry):
            # For Entry widgets, use native clipboard operations
            widget.bind('<Control-c>', lambda e: widget.event_generate('<<Copy>>'))
            widget.bind('<Control-x>', lambda e: widget.event_generate('<<Cut>>'))
            widget.bind('<Control-v>', lambda e: widget.event_generate('<<Paste>>'))
            widget.bind('<Control-a>', lambda e: widget.select_range(0, tk.END))
        elif isinstance(widget, scrolledtext.ScrolledText):
            # For ScrolledText widgets (chat_area)
            widget.bind('<Control-c>', lambda e: widget.event_generate('<<Copy>>'))
            widget.bind('<Control-a>', lambda e: widget.tag_add(tk.SEL, "1.0", tk.END))
    
    def _apply_theme(self):
        """Apply current theme throughout the interface"""
        # This is handled during initialization
        # Full theme reapplication would require recreating widgets
        pass
