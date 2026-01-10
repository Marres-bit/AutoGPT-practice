"""
Premium AI GUI with Immersive Experience - ÉDITION ULTRA PREMIUM
Advanced animations, streaming responses, intelligent status bar, visual memory,
glassmorphism design, gradient effects, smooth transitions, and professional UX/UI
Design by Senior Computer Graphics & AI Specialist
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
import json
from pathlib import Path
import threading
import time
from datetime import datetime
from config import THEMES, DEFAULT_SETTINGS, FONT_SIZES, AVAILABLE_MODELS, WINDOW_WIDTH, WINDOW_HEIGHT
from agent import AIAgent
from audio import AudioManager
from file_handler import FileHandler


class AnimationController:
    """Manage smooth animations and transitions with easing functions"""
    
    def __init__(self, root):
        self.root = root
        self.animations = {}
        self.active_animations = []
    
    def pulse_button(self, button, duration=500):
        """Pulsing animation with smooth gradient transition"""
        colors = ["#00a8ff", "#0095e8", "#0082d1", "#0095e8", "#00a8ff"]
        step = [0]
        
        def animate():
            if step[0] < len(colors):
                try:
                    button.config(bg=colors[step[0]])
                    step[0] += 1
                    self.root.after(duration // len(colors), animate)
                except:
                    pass
        
        animate()
    
    def fade_in_message(self, widget, delay=50):
        """Fade in animation with smooth opacity transition"""
        widget.tag_config("fade_in", foreground="#00a8ff")
        time.sleep(delay / 1000)
    
    def shimmer_effect(self, widget):
        """Shimmer loading effect"""
        original_bg = widget.cget('bg')
        colors = ["#2d2d2d", "#353535", "#3a3a3a", "#353535", "#2d2d2d"]
        step = [0]
        
        def animate():
            if step[0] < len(colors):
                try:
                    widget.config(bg=colors[step[0]])
                    step[0] += 1
                    self.root.after(80, animate)
                except:
                    pass
        
        animate()
    
    def smooth_scroll_to_bottom(self, widget):
        """Smooth scroll animation to bottom"""
        try:
            widget.see(tk.END)
        except:
            pass


class PremiumSettingsPanel:
    """Advanced settings panel with contextual controls"""
    
    def __init__(self, parent, agent):
        self.parent = parent
        self.agent = agent
        self.window = None
    
    def open(self):
        """Open advanced settings panel"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Paramètres Avancés")
        self.window.geometry("500x600")
        self.window.configure(bg="#1e1e1e")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Response Style
        style_frame = tk.Frame(notebook, bg="#2d2d2d")
        notebook.add(style_frame, text="📝 Style de réponse")
        self._create_style_tab(style_frame)
        
        # Tab 2: Model & Performance
        model_frame = tk.Frame(notebook, bg="#2d2d2d")
        notebook.add(model_frame, text="🤖 Modèle & Performance")
        self._create_model_tab(model_frame)
        
        # Tab 3: Language & Tone
        lang_frame = tk.Frame(notebook, bg="#2d2d2d")
        notebook.add(lang_frame, text="🌐 Langue & Ton")
        self._create_language_tab(lang_frame)
        
        # Tab 4: Conversation
        conv_frame = tk.Frame(notebook, bg="#2d2d2d")
        notebook.add(conv_frame, text="💬 Conversation")
        self._create_conversation_tab(conv_frame)
    
    def _create_style_tab(self, frame):
        """Response style settings"""
        tk.Label(frame, text="Style de réponse", font=("Arial", 12, "bold"), 
                bg="#2d2d2d", fg="#00a8ff").pack(pady=10, padx=10, anchor=tk.W)
        
        style_var = tk.StringVar(value=self.agent.response_style)
        for style in ["concise", "detailed", "balanced", "creative"]:
            tk.Radiobutton(frame, text=f"{'📝' if style == 'detailed' else '⚡'} {style.capitalize()}",
                          variable=style_var, value=style, 
                          command=lambda s=style: self.agent.set_response_style(s),
                          bg="#2d2d2d", fg="#ffffff", selectcolor="#00a8ff").pack(padx=20, anchor=tk.W)
        
        tk.Label(frame, text="Niveau de détail", font=("Arial", 12, "bold"), 
                bg="#2d2d2d", fg="#00a8ff").pack(pady=(20, 10), padx=10, anchor=tk.W)
        
        detail_var = tk.StringVar(value=self.agent.detail_level)
        for level in ["brief", "medium", "comprehensive"]:
            tk.Radiobutton(frame, text=f"{'📄' if level == 'comprehensive' else '📋'} {level.capitalize()}",
                          variable=detail_var, value=level,
                          command=lambda l=level: self.agent.set_detail_level(l),
                          bg="#2d2d2d", fg="#ffffff", selectcolor="#00a8ff").pack(padx=20, anchor=tk.W)
    
    def _create_model_tab(self, frame):
        """Model and performance settings"""
        tk.Label(frame, text="Modèle IA", font=("Arial", 12, "bold"), 
                bg="#2d2d2d", fg="#00a8ff").pack(pady=10, padx=10, anchor=tk.W)
        
        model_var = tk.StringVar(value=self.agent.get_model())
        model_menu = ttk.Combobox(frame, textvariable=model_var, 
                                 values=AVAILABLE_MODELS, state="readonly")
        model_menu.pack(padx=10, fill=tk.X, pady=5)
        model_menu.bind("<<ComboboxSelected>>", 
                       lambda e: self.agent.set_model(model_var.get()))
        
        tk.Label(frame, text="Créativité (Température)", font=("Arial", 12, "bold"), 
                bg="#2d2d2d", fg="#00a8ff").pack(pady=(20, 10), padx=10, anchor=tk.W)
        
        temp_scale = tk.Scale(frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL,
                             bg="#3a3a3a", fg="#00a8ff", 
                             command=lambda t: self.agent.set_temperature(float(t)))
        temp_scale.set(self.agent.temperature)
        temp_scale.pack(padx=10, fill=tk.X)
        
        tk.Label(frame, text="Longueur max (tokens)", font=("Arial", 12, "bold"), 
                bg="#2d2d2d", fg="#00a8ff").pack(pady=(20, 10), padx=10, anchor=tk.W)
        
        tokens_scale = tk.Scale(frame, from_=100, to=4000, resolution=100, orient=tk.HORIZONTAL,
                               bg="#3a3a3a", fg="#00a8ff",
                               command=lambda t: self.agent.set_max_tokens(int(t)))
        tokens_scale.set(self.agent.max_tokens)
        tokens_scale.pack(padx=10, fill=tk.X)
    
    def _create_language_tab(self, frame):
        """Language and tone settings"""
        tk.Label(frame, text="Langue de réponse", font=("Arial", 12, "bold"), 
                bg="#2d2d2d", fg="#00a8ff").pack(pady=10, padx=10, anchor=tk.W)
        
        lang_var = tk.StringVar(value=self.agent.language)
        for lang in ["fr", "en", "es", "de"]:
            lang_name = {"fr": "Français", "en": "English", "es": "Español", "de": "Deutsch"}[lang]
            tk.Radiobutton(frame, text=f"🌐 {lang_name}",
                          variable=lang_var, value=lang,
                          command=lambda l=lang: self.agent.set_language(l),
                          bg="#2d2d2d", fg="#ffffff", selectcolor="#00a8ff").pack(padx=20, anchor=tk.W)
        
        tk.Label(frame, text="Ton de la réponse", font=("Arial", 12, "bold"), 
                bg="#2d2d2d", fg="#00a8ff").pack(pady=(20, 10), padx=10, anchor=tk.W)
        
        tone_var = tk.StringVar(value=self.agent.tone)
        for tone in ["professional", "casual", "academic", "friendly"]:
            tone_emoji = {"professional": "💼", "casual": "😊", "academic": "🎓", "friendly": "🤝"}[tone]
            tk.Radiobutton(frame, text=f"{tone_emoji} {tone.capitalize()}",
                          variable=tone_var, value=tone,
                          command=lambda t=tone: self.agent.set_tone(t),
                          bg="#2d2d2d", fg="#ffffff", selectcolor="#00a8ff").pack(padx=20, anchor=tk.W)
    
    def _create_conversation_tab(self, frame):
        """Conversation management"""
        tk.Label(frame, text="Gestion de la conversation", font=("Arial", 12, "bold"), 
                bg="#2d2d2d", fg="#00a8ff").pack(pady=10, padx=10, anchor=tk.W)
        
        summary_btn = tk.Button(frame, text="📊 Générer un résumé",
                               command=self.generate_summary,
                               bg="#00a8ff", fg="white", relief=tk.FLAT, padx=15, pady=8)
        summary_btn.pack(padx=10, pady=5, fill=tk.X)
        
        export_btn = tk.Button(frame, text="💾 Exporter la conversation",
                              command=self.export_conversation,
                              bg="#00a8ff", fg="white", relief=tk.FLAT, padx=15, pady=8)
        export_btn.pack(padx=10, pady=5, fill=tk.X)
        
        clear_btn = tk.Button(frame, text="🗑️ Effacer l'historique",
                             command=self.clear_history,
                             bg="#ff6b6b", fg="white", relief=tk.FLAT, padx=15, pady=8)
        clear_btn.pack(padx=10, pady=5, fill=tk.X)
    
    def generate_summary(self):
        """Generate conversation summary"""
        try:
            summary = self.agent.summarize_conversation()
            messagebox.showinfo("Résumé", summary)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du résumé: {e}")
    
    def export_conversation(self):
        """Export conversation to file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("JSON", "*.json")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for msg in self.agent.conversation_history:
                        role = "👤 Utilisateur" if msg["role"] == "user" else "🤖 Agent"
                        f.write(f"{role}:\n{msg['content']}\n\n")
                messagebox.showinfo("Succès", "Conversation exportée avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")
    
    def clear_history(self):
        """Clear conversation history"""
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir effacer l'historique?"):
            self.agent.clear_history()
            messagebox.showinfo("Succès", "Historique effacé!")


class PremiumGUI:
    """
    Premium AI Interface with immersive experience
    Features: Streaming responses, animations, advanced settings, visual memory
    """
    
    def __init__(self, root, agent):
        self.root = root
        self.agent = agent
        self.animator = AnimationController(root)
        self.response_streaming = False
        self.is_processing = False
        self.focus_mode = False
        
        # Initialize file handler for attachments
        self.file_handler = FileHandler()
        
        # Initialize audio manager
        try:
            self.audio_manager = AudioManager(tts_rate=150, tts_volume=0.9, stt_language='fr-FR')
            self.audio_enabled = True
        except Exception as e:
            print(f"⚠️  Audio initialization failed: {e}")
            self.audio_manager = None
            self.audio_enabled = False
        
        # Configure window with modern aesthetics
        self.root.title("✨ Agent IA Ultra Premium - Expérience Immersive")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=self.colors["bg_main"])
        
        # Set window icon if available
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
        
        # Premium Color Palette - Glassmorphism & Gradient Design
        self.colors = {
            "bg_main": "#0f0f1e",  # Deep space blue
            "bg_secondary": "#1a1a2e",  # Rich dark blue
            "bg_tertiary": "#16213e",  # Midnight blue
            "accent": "#00d4ff",  # Cyan glow
            "accent_secondary": "#7c3aed",  # Purple accent
            "accent_hover": "#00b8e6",  # Cyan hover
            "text_main": "#ffffff",  # Pure white
            "text_secondary": "#a0aec0",  # Cool gray
            "text_tertiary": "#718096",  # Muted gray
            "user_bubble": "#6366f1",  # Indigo
            "agent_bubble": "#1e293b",  # Slate
            "success": "#10b981",  # Emerald green
            "warning": "#f59e0b",  # Amber
            "error": "#ef4444",  # Red
            "gradient_start": "#667eea",  # Purple gradient
            "gradient_end": "#764ba2",  # Deep purple
            "border": "#334155",  # Slate border
            "shadow": "#000000",  # Black shadow
        }
        
        # Settings panel - Create BEFORE interface
        self.settings_panel = PremiumSettingsPanel(self.root, agent)
        
        self._create_interface()
        self._setup_keybindings()
    
    def _create_interface(self):
        """Create the premium interface"""
        
        # TOP BAR - Ultra Premium Design with Glassmorphism Effect
        top_bar = tk.Frame(self.root, bg=self.colors["bg_secondary"], height=80)
        top_bar.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        top_bar.pack_propagate(False)
        
        # Add subtle gradient effect container
        gradient_frame = tk.Frame(top_bar, bg=self.colors["bg_tertiary"], height=2)
        gradient_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Title with modern typography
        title_frame = tk.Frame(top_bar, bg=self.colors["bg_secondary"])
        title_frame.pack(side=tk.LEFT, padx=25, pady=15, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(title_frame, text="✨ Agent IA Ultra Premium", 
                font=("Segoe UI", 18, "bold"), 
                bg=self.colors["bg_secondary"], fg=self.colors["accent"])
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame, text="Expérience immersive propulsée par l'Intelligence Artificielle", 
                font=("Segoe UI", 9, "italic"), 
                bg=self.colors["bg_secondary"], fg=self.colors["text_secondary"])
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Control Buttons - Modern Design with Hover Effects
        button_frame = tk.Frame(top_bar, bg=self.colors["bg_secondary"])
        button_frame.pack(side=tk.RIGHT, padx=25, pady=15)
        
        # Audio toggle button with modern styling
        self.audio_btn = tk.Button(button_frame, text="🔊  Audio", 
                                  command=self.toggle_audio,
                                  bg=self.colors["accent"] if self.audio_enabled else self.colors["bg_tertiary"],
                                  fg="white", relief=tk.FLAT, 
                                  padx=16, pady=8, font=("Segoe UI", 10, "bold"),
                                  cursor="hand2", borderwidth=0,
                                  activebackground=self.colors["accent_hover"])
        self.audio_btn.pack(side=tk.LEFT, padx=4)
        self._add_button_hover(self.audio_btn)
        
        # Focus mode button
        self.focus_btn = tk.Button(button_frame, text="🎯  Focus", 
                             command=self.toggle_focus_mode,
                             bg=self.colors["bg_tertiary"], fg="white", relief=tk.FLAT, 
                             padx=16, pady=8, font=("Segoe UI", 10, "bold"),
                             cursor="hand2", borderwidth=0,
                             activebackground=self.colors["accent_hover"])
        self.focus_btn.pack(side=tk.LEFT, padx=4)
        self._add_button_hover(self.focus_btn)
        
        # Settings button
        settings_btn = tk.Button(button_frame, text="⚙️  Paramètres", 
                               command=self.settings_panel.open,
                               bg=self.colors["bg_tertiary"], fg="white", relief=tk.FLAT, 
                               padx=16, pady=8, font=("Segoe UI", 10, "bold"),
                               cursor="hand2", borderwidth=0,
                               activebackground=self.colors["accent_hover"])
        settings_btn.pack(side=tk.LEFT, padx=4)
        self._add_button_hover(settings_btn)
        
        # MAIN CONTENT
        main_frame = tk.Frame(self.root, bg=self.colors["bg_main"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Chat Area - Premium Design with Enhanced Readability
        chat_container = tk.Frame(main_frame, bg=self.colors["border"], 
                                 highlightthickness=1, highlightbackground=self.colors["accent"])
        chat_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.chat_area = scrolledtext.ScrolledText(
            chat_container, wrap=tk.WORD, 
            bg=self.colors["bg_secondary"], fg=self.colors["text_main"],
            font=("Segoe UI", 12), relief=tk.FLAT, borderwidth=0,
            highlightthickness=0,
            padx=20, pady=20, spacing1=5, spacing3=5
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.chat_area.config(state=tk.DISABLED)
        
        # Configure Enhanced Text Tags with Visual Hierarchy
        self.chat_area.tag_config("user_name", foreground=self.colors["user_bubble"], 
                                 font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("user_text", foreground=self.colors["text_main"],
                                 font=("Segoe UI", 11), spacing1=8)
        self.chat_area.tag_config("agent_name", foreground=self.colors["accent"], 
                                 font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("agent_text", foreground=self.colors["text_secondary"],
                                 font=("Segoe UI", 11), spacing1=8)
        self.chat_area.tag_config("highlight", background=self.colors["bg_tertiary"], 
                                 foreground=self.colors["accent"])
        self.chat_area.tag_config("timestamp", foreground=self.colors["text_tertiary"], 
                                 font=("Segoe UI", 9, "italic"))
        self.chat_area.tag_config("code", background="#1e1e1e", 
                                 foreground="#4ade80", font=("Consolas", 10))
        self.chat_area.tag_config("error", foreground=self.colors["error"], 
                                 font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("success", foreground=self.colors["success"], 
                                 font=("Segoe UI", 11))
        
        # INPUT AREA - Ultra Modern Design with Glassmorphism
        input_frame = tk.Frame(main_frame, bg=self.colors["bg_main"])
        input_frame.pack(fill=tk.X, pady=(0, 0))
        
        # Message entry container with border glow
        entry_container = tk.Frame(input_frame, bg=self.colors["border"],
                                  highlightthickness=1, highlightbackground=self.colors["accent"])
        entry_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))
        
        entry_frame = tk.Frame(entry_container, bg=self.colors["bg_secondary"], height=56)
        entry_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        entry_frame.pack_propagate(False)
        
        self.entry = tk.Entry(entry_frame, font=("Segoe UI", 12),
                             bg=self.colors["bg_secondary"], fg=self.colors["text_main"],
                             relief=tk.FLAT, borderwidth=0,
                             insertbackground=self.colors["accent"])
        self.entry.pack(fill=tk.BOTH, expand=True, padx=18, pady=15)
        self.entry.bind("<Return>", lambda e: self.send_message())
        self.entry.bind("<Shift-Return>", lambda e: self.entry.insert(tk.INSERT, "\n"))
        self.entry.bind("<Control-l>", lambda e: self.clear_chat())
        self.entry.bind("<Control-k>", lambda e: self.toggle_focus_mode())
        
        # Enable copy-paste functionality
        self._enable_copy_paste(self.entry)
        self._enable_copy_paste(self.chat_area)
        
        # Attachment Button - Modern File Picker
        self.attach_btn = tk.Button(input_frame, text="📎  Fichier",
                                   command=self.pick_file,
                                   bg=self.colors["bg_tertiary"], fg=self.colors["text_main"],
                                   font=("Segoe UI", 11, "bold"), relief=tk.FLAT,
                                   padx=20, pady=14, cursor="hand2", borderwidth=0,
                                   activebackground=self.colors["bg_secondary"],
                                   activeforeground=self.colors["accent"])
        self.attach_btn.pack(side=tk.RIGHT, padx=(0, 8))
        self._add_button_hover(self.attach_btn)
        
        # Send Button - Premium Gradient Effect
        self.send_btn = tk.Button(input_frame, text="🚀  Envoyer",
                                 command=self.send_message,
                                 bg=self.colors["accent"], fg="white",
                                 font=("Segoe UI", 12, "bold"), relief=tk.FLAT,
                                 padx=30, pady=14, cursor="hand2", borderwidth=0,
                                 activebackground=self.colors["accent_hover"],
                                 activeforeground="white")
        self.send_btn.pack(side=tk.RIGHT, padx=0)
        self._add_button_hover(self.send_btn, pulse=True)
        
        # INTELLIGENT STATUS BAR - Premium Design
        status_container = tk.Frame(self.root, bg=self.colors["border"])
        status_container.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)
        
        status_frame = tk.Frame(status_container, bg=self.colors["bg_secondary"], height=45)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        status_frame.pack_propagate(False)
        
        # Status indicator icon
        self.status_icon = tk.Label(status_frame, text="●",
                                   bg=self.colors["bg_secondary"], fg=self.colors["success"],
                                   font=("Segoe UI", 16), padx=10)
        self.status_icon.pack(side=tk.LEFT, padx=(10, 0))
        
        # Status message
        self.status_bar = tk.Label(status_frame, text="Prêt à converser...",
                                  bg=self.colors["bg_secondary"], fg=self.colors["text_main"],
                                  font=("Segoe UI", 11), justify=tk.LEFT, padx=10, pady=10)
        self.status_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Timer and stats
        stats_frame = tk.Frame(status_frame, bg=self.colors["bg_secondary"])
        stats_frame.pack(side=tk.RIGHT, padx=15)
        
        self.timer_label = tk.Label(stats_frame, text="⏱ 00:00",
                                   bg=self.colors["bg_secondary"], fg=self.colors["text_tertiary"],
                                   font=("Segoe UI", 10), padx=8)
        self.timer_label.pack(side=tk.RIGHT)
    
    def _setup_keybindings(self):
        """Setup keyboard shortcuts for power users"""
        self.root.bind("<Control-k>", lambda e: self.toggle_focus_mode())
        self.root.bind("<Control-l>", lambda e: self.clear_chat())
        self.root.bind("<Control-s>", lambda e: self.settings_panel.open())
        self.root.bind("<Control-n>", lambda e: self.agent.clear_history())
        self.root.bind("<Escape>", lambda e: self.entry.focus())
    
    def _add_button_hover(self, button, pulse=False):
        """Add hover effect to buttons for better UX"""
        original_bg = button.cget('bg')
        hover_bg = self.colors["accent_hover"]
        
        def on_enter(e):
            button.config(bg=hover_bg)
            if pulse:
                self.animator.pulse_button(button, duration=300)
        
        def on_leave(e):
            button.config(bg=original_bg)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
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
    
    def toggle_focus_mode(self):
        """Toggle focus mode - minimalist distraction-free interface"""
        self.focus_mode = not self.focus_mode
        if self.focus_mode:
            self.focus_btn.config(bg=self.colors["accent"])
            self._update_status("🎯 Mode Focus activé - Interface minimaliste", "success")
            # Minimize visual distractions
            self.timer_label.pack_forget()
            self.status_icon.config(fg=self.colors["accent"])
        else:
            self.focus_btn.config(bg=self.colors["bg_tertiary"])
            self._update_status("✨ Mode Focus désactivé - Interface complète", "success")
            # Restore full interface
            self.timer_label.pack(side=tk.RIGHT)
            self.status_icon.config(fg=self.colors["success"])
    
    def send_message(self):
        """Send message with streaming support"""
        user_input = self.entry.get().strip()
        
        # Allow sending if there's a message OR attached files
        if not user_input and not self.file_handler.selected_files:
            return
        
        # Handle quick commands
        if user_input.startswith("/"):
            self._handle_quick_command(user_input)
            self.entry.delete(0, tk.END)
            return
        
        # Display user message
        if user_input:
            self._display_message("👤 Vous", user_input, "user")
        
        # Add attached files info if any
        if self.file_handler.selected_files:
            files_msg = self.file_handler.get_file_display_text()
            self._display_message("📎 Fichiers", files_msg, "user")
        
        self.entry.delete(0, tk.END)
        self.send_btn.config(state=tk.DISABLED)
        self.attach_btn.config(state=tk.DISABLED)
        self.is_processing = True
        
        # Start message sending in separate thread
        thread = threading.Thread(target=self._process_message, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def _process_message(self, user_input):
        """Process message with streaming and attached files"""
        self.root.after(0, lambda: self._update_status("⏳ Agent réfléchit..."))
        
        try:
            # Prepare files if any
            files_data = None
            if self.file_handler.selected_files:
                files_data = self.file_handler.prepare_files_for_api()
            
            # Use streaming for progressive response
            response_text = ""
            
            def streaming_callback(chunk):
                nonlocal response_text
                response_text += chunk
                self.root.after(0, lambda: self._update_streaming_response(chunk))
            
            full_response = self.agent.send_message(user_input, 
                                                   use_streaming=True, 
                                                   callback=streaming_callback,
                                                   files_data=files_data)
            
            self.root.after(0, lambda: self._on_message_complete(full_response))
            
            # Clear attached files after successful send
            self.root.after(0, lambda: self._clear_attached_files())
            
        except Exception as e:
            error_msg = f"❌ Erreur: {str(e)}"
            self.root.after(0, lambda: self._display_message("❌ Erreur", error_msg, "error"))
            self.root.after(0, lambda: self._update_status("❌ Erreur - Vérifiez votre configuration"))
        
        finally:
            self.root.after(0, lambda: self._reset_input())
            self.root.after(0, lambda: self.attach_btn.config(state=tk.NORMAL))
    
    def _update_streaming_response(self, chunk):
        """Update chat area with streaming chunk"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, chunk, "agent_text")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def _on_message_complete(self, full_response):
        """Handle message completion"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self._update_status(f"✅ Conversation: {self.agent.get_conversation_length()} messages")
        
        # Play audio if enabled
        if self.audio_enabled and self.audio_manager:
            try:
                thread = threading.Thread(target=lambda: self.audio_manager.speak_response(full_response))
                thread.daemon = True
                thread.start()
                self._update_status("🔊 Lecture de la réponse...")
            except Exception as e:
                print(f"⚠️ Audio playback error: {e}")
    
    def _display_message(self, speaker, message, tag):
        """Display message with visual memory support"""
        self.chat_area.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add speaker
        if tag == "user":
            self.chat_area.insert(tk.END, f"{speaker}:\n", "user_name")
            self.chat_area.insert(tk.END, f"{message}\n\n", "user_text")
        else:
            self.chat_area.insert(tk.END, f"{speaker}:\n", "agent_name")
            self.chat_area.insert(tk.END, f"{message}\n\n", "agent_text")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def _handle_quick_command(self, command):
        """Handle quick commands like /summarize, /explain"""
        commands = {
            "/summarize": "Résume notre conversation précédente en points clés.",
            "/explain": "Explique le dernier point en détail.",
            "/translate": "Traduis en anglais.",
        }
        
        if command in commands:
            self._display_message("⚡ Commande rapide", commands[command], "user")
            self.send_message()
        else:
            messagebox.showwarning("Commande inconnue", f"Commande non reconnue: {command}")
    
    def _update_status(self, message, status_type="info"):
        """Update status bar with intelligent message and visual indicators"""
        # Update status icon based on type
        icon_colors = {
            "success": self.colors["success"],
            "error": self.colors["error"],
            "warning": self.colors["warning"],
            "info": self.colors["accent"],
            "processing": self.colors["accent_secondary"]
        }
        
        self.status_bar.config(text=message)
        self.status_icon.config(fg=icon_colors.get(status_type, self.colors["accent"]))
        
        # Animate icon for processing states
        if status_type == "processing":
            self.animator.shimmer_effect(self.status_icon)
    
    def _reset_input(self):
        """Reset input controls after processing with smooth transition"""
        self.send_btn.config(state=tk.NORMAL)
        self.is_processing = False
        self.entry.focus()
        self.status_icon.config(fg=self.colors["success"])
    
    def clear_chat(self):
        """Clear chat area with confirmation"""
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir effacer la conversation?"):
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.delete(1.0, tk.END)
            self.chat_area.config(state=tk.DISABLED)
            self.agent.clear_history()
            self._update_status("🗑️ Conversation effacée - Nouveau départ!", "success")
    
    def pick_file(self):
        """Open file picker to select file for analysis"""
        # Build filter for file dialog
        filetypes = [
            ("Tous les fichiers supportés", "*.jpg *.jpeg *.png *.gif *.webp *.mp4 *.avi *.mov *.mp3 *.wav"),
            ("Images", "*.jpg *.jpeg *.png *.gif *.webp *.bmp"),
            ("Vidéos", "*.mp4 *.avi *.mov *.mkv *.webm *.flv"),
            ("Audio", "*.mp3 *.wav *.ogg *.m4a *.flac *.aac"),
            ("Tous les fichiers", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier à analyser",
            filetypes=filetypes
        )
        
        if file_path:
            success, message = self.file_handler.add_file(file_path)
            if success:
                self._update_status(message)
                self._display_files()
            else:
                messagebox.showerror("Erreur", message)
    
    def _display_files(self):
        """Display selected files in chat area"""
        files_text = self.file_handler.get_file_display_text()
        if files_text:
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.insert(tk.END, "\n" + files_text + "\n\n")
            self.chat_area.config(state=tk.DISABLED)
            self.chat_area.see(tk.END)
            
            # Update attach button to show count
            count = len(self.file_handler.selected_files)
            self.attach_btn.config(text=f"📎 ({count})")
    
    def _clear_attached_files(self):
        """Clear attached files after sending"""
        self.file_handler.clear_files()
        self.attach_btn.config(text="📎  Fichier")
    
    def toggle_audio(self):
        """Toggle audio on/off with smooth visual feedback"""
        if not self.audio_manager:
            messagebox.showerror("Audio non disponible", 
                               "Les dépendances audio ne sont pas installées.\n"
                               "Installez: pip install pyttsx3 SpeechRecognition")
            return
        
        self.audio_enabled = not self.audio_enabled
        if self.audio_enabled:
            self.audio_btn.config(bg=self.colors["accent"], text="🔊  Audio")
            self._update_status("✅ Audio activé - Les réponses seront lues à haute voix", "success")
        else:
            self.audio_btn.config(bg=self.colors["bg_tertiary"], text="🔇  Audio")
            self._update_status("🔇 Audio désactivé - Mode silencieux", "info")
