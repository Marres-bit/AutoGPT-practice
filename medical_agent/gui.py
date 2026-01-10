"""
Medical AI Agent - Premium GUI avec Bob l'éponge
Interface moderne pour l'agent médical autonome
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
from datetime import datetime
from pathlib import Path

from medical_agent.agent import MedicalAIAgent
from medical_agent.database import MedicalDatabase
from medical_agent.scheduler import MedicalScheduler
from medical_agent.commands import CommandHandler
from medical_agent.config import *


class MedicalGUI:
    """Interface graphique premium pour l'agent médical"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"🧽 {AGENT_NAME} - Assistant Médical Autonome")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=THEME["bg_main"])
        
        # Initialiser les composants
        print("🔄 Initialisation des composants...")
        self.agent = MedicalAIAgent()
        self.database = MedicalDatabase()
        self.scheduler = MedicalScheduler(self.agent, self.database)
        self.command_handler = CommandHandler(self.agent, self.database, self.scheduler)
        
        # Démarrer le scheduler automatique
        self.scheduler.start()
        
        # Conversation history
        self.conversation_history = []
        
        # Créer l'interface
        self._create_interface()
        
        # Message de bienvenue
        self._display_welcome_message()
        
        print("✅ Interface médicale prête!")
    
    def _create_interface(self):
        """Créer l'interface utilisateur"""
        
        # HEADER avec Bob l'éponge
        header = tk.Frame(self.root, bg=THEME["accent"], height=100)
        header.pack(side=tk.TOP, fill=tk.X)
        header.pack_propagate(False)
        
        # Titre avec emoji Bob
        title_frame = tk.Frame(header, bg=THEME["accent"])
        title_frame.pack(expand=True)
        
        tk.Label(title_frame, text="🧽", font=("Segoe UI", 48),
                bg=THEME["accent"]).pack(side=tk.LEFT, padx=10)
        
        title_text = tk.Frame(title_frame, bg=THEME["accent"])
        title_text.pack(side=tk.LEFT, padx=10)
        
        tk.Label(title_text, text="MediGenius AI", 
                font=("Segoe UI", 20, "bold"),
                bg=THEME["accent"], fg="white").pack(anchor=tk.W)
        
        tk.Label(title_text, text="Assistant Médical Autonome • 3 Leçons/Semaine", 
                font=("Segoe UI", 11),
                bg=THEME["accent"], fg="white").pack(anchor=tk.W)
        
        # SIDEBAR - Commandes rapides
        sidebar = tk.Frame(self.root, bg=THEME["bg_secondary"], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="⚡ COMMANDES RAPIDES", 
                font=("Segoe UI", 12, "bold"),
                bg=THEME["bg_secondary"], fg=THEME["text_main"]).pack(pady=15, padx=10)
        
        # Boutons de commandes
        commands_buttons = [
            ("📚 Nouvelle Leçon", "/lesson", THEME["accent"]),
            ("🔍 Rechercher Maladie", "/disease ", THEME["success"]),
            ("📝 Générer Quiz", "/quiz ", THEME["warning"]),
            ("💊 Pharmacologie", "/pharmacology ", THEME["accent"]),
            ("🚨 Urgence", "/emergency ", THEME["error"]),
            ("📊 Statistiques", "/statistics", THEME["accent"]),
            ("📋 Lister Leçons", "/list", THEME["success"]),
            ("❓ Aide", "/help", THEME["text_secondary"])
        ]
        
        for label, cmd, color in commands_buttons:
            btn = tk.Button(sidebar, text=label,
                          command=lambda c=cmd: self._quick_command(c),
                          bg=color, fg="white",
                          font=("Segoe UI", 10, "bold"),
                          relief=tk.FLAT, padx=15, pady=10,
                          cursor="hand2", anchor=tk.W)
            btn.pack(fill=tk.X, padx=10, pady=5)
            self._add_hover_effect(btn, color)
        
        # Status du scheduler
        tk.Label(sidebar, text="⏰ SCHEDULER", 
                font=("Segoe UI", 11, "bold"),
                bg=THEME["bg_secondary"], fg=THEME["text_main"]).pack(pady=(20, 10), padx=10)
        
        self.scheduler_status = tk.Label(sidebar, text="Chargement...", 
                                        font=("Segoe UI", 9),
                                        bg=THEME["bg_secondary"], fg=THEME["text_secondary"],
                                        justify=tk.LEFT, wraplength=220)
        self.scheduler_status.pack(padx=10, pady=5)
        
        self._update_scheduler_status()
        
        # MAIN CONTENT
        main_frame = tk.Frame(self.root, bg=THEME["bg_main"])
        main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Chat Area
        chat_container = tk.Frame(main_frame, bg=THEME["border"], 
                                 highlightthickness=2, highlightbackground=THEME["accent"])
        chat_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.chat_area = scrolledtext.ScrolledText(
            chat_container, wrap=tk.WORD,
            bg=THEME["bg_card"], fg=THEME["text_main"],
            font=("Segoe UI", 11), relief=tk.FLAT, borderwidth=0,
            padx=20, pady=20, spacing1=5, spacing3=5
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.chat_area.config(state=tk.DISABLED)
        
        # Configure tags
        self.chat_area.tag_config("user", foreground=THEME["accent"], font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("agent", foreground=THEME["success"], font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("system", foreground=THEME["warning"], font=("Segoe UI", 10, "italic"))
        self.chat_area.tag_config("command", foreground=THEME["text_secondary"], font=("Segoe UI", 10))
        
        # Input Area
        input_frame = tk.Frame(main_frame, bg=THEME["bg_main"])
        input_frame.pack(fill=tk.X)
        
        entry_container = tk.Frame(input_frame, bg=THEME["border"],
                                  highlightthickness=2, highlightbackground=THEME["accent"])
        entry_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.entry = tk.Entry(entry_container, font=("Segoe UI", 12),
                             bg=THEME["bg_card"], fg=THEME["text_main"],
                             relief=tk.FLAT, borderwidth=0)
        self.entry.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        self.entry.bind("<Return>", lambda e: self.send_message())
        
        # Send button
        self.send_btn = tk.Button(input_frame, text="🚀 Envoyer",
                                  command=self.send_message,
                                  bg=THEME["accent"], fg="white",
                                  font=("Segoe UI", 12, "bold"),
                                  relief=tk.FLAT, padx=30, pady=12,
                                  cursor="hand2")
        self.send_btn.pack(side=tk.RIGHT)
        self._add_hover_effect(self.send_btn, THEME["accent"])
        
        # Status bar
        status_frame = tk.Frame(self.root, bg=THEME["bg_secondary"], height=40)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_bar = tk.Label(status_frame, text="✅ Prêt • Scheduler actif",
                                   bg=THEME["bg_secondary"], fg=THEME["success"],
                                   font=("Segoe UI", 10), padx=15)
        self.status_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def _add_hover_effect(self, button, color):
        """Ajoute un effet hover sur les boutons"""
        def on_enter(e):
            button.config(bg=THEME["accent_hover"])
        
        def on_leave(e):
            button.config(bg=color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def _display_welcome_message(self):
        """Affiche le message de bienvenue"""
        welcome = f"""� Bienvenue chez MediGenius AI!

Je suis ton assistant médical autonome qui génère automatiquement 3 leçons par semaine (Lundi, Mercredi, Vendredi à 9h).

📚 FONCTIONNALITÉS:
• Génération automatique de leçons médicales
• Recherche de maladies et pathologies
• Quiz interactifs
• Protocoles de traitement
• Informations pharmacologiques
• Protocoles d'urgence

⚡ COMMANDES DISPONIBLES:
Tape /help pour voir toutes les commandes ou utilise les boutons à gauche!

🤖 SCHEDULER AUTOMATIQUE:
Le système génère {LESSONS_PER_WEEK} leçons par semaine automatiquement.
Prochaine génération: {self.scheduler._get_next_generation_time()}

💬 Tu peux aussi me poser des questions médicales directement!
"""
        
        self._display_message("� MediGenius AI", welcome, "agent")
    
    def _quick_command(self, command: str):
        """Exécute une commande rapide"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, command)
        if not command.endswith(" "):
            self.send_message()
        else:
            self.entry.focus()
    
    def send_message(self):
        """Envoie un message ou exécute une commande"""
        user_input = self.entry.get().strip()
        
        if not user_input:
            return
        
        # Afficher le message utilisateur
        self._display_message("👤 Vous", user_input, "user")
        self.entry.delete(0, tk.END)
        
        # Désactiver le bouton
        self.send_btn.config(state=tk.DISABLED)
        self._update_status("⏳ Traitement en cours...")
        
        # Traiter dans un thread séparé
        thread = threading.Thread(target=self._process_message, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def _process_message(self, user_input: str):
        """Traite le message dans un thread séparé"""
        try:
            # Vérifier si c'est une commande
            if user_input.startswith('/'):
                parts = user_input.split(' ', 1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                
                response = self.command_handler.execute(command, args)
            else:
                # Chat normal
                response = self.agent.chat(user_input, self.conversation_history)
                
                # Ajouter à l'historique
                self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": response})
            
            # Afficher la réponse
            self.root.after(0, lambda: self._display_message("� MediGenius AI", response, "agent"))
            self.root.after(0, lambda: self._update_status("✅ Prêt"))
            
        except Exception as e:
            error_msg = f"❌ Erreur: {e}"
            self.root.after(0, lambda: self._display_message("❌ Erreur", error_msg, "system"))
            self.root.after(0, lambda: self._update_status("❌ Erreur"))
        
        finally:
            self.root.after(0, lambda: self.send_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.entry.focus())
    
    def _display_message(self, speaker: str, message: str, tag: str):
        """Affiche un message dans le chat"""
        self.chat_area.config(state=tk.NORMAL)
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_area.insert(tk.END, f"[{timestamp}] ", "command")
        
        # Speaker
        self.chat_area.insert(tk.END, f"{speaker}:\n", tag)
        
        # Message
        self.chat_area.insert(tk.END, f"{message}\n\n")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def _update_status(self, message: str):
        """Met à jour la barre de statut"""
        self.status_bar.config(text=message)
    
    def _update_scheduler_status(self):
        """Met à jour le statut du scheduler"""
        status = self.scheduler.get_status()
        stats = self.scheduler.get_weekly_stats()
        
        status_text = f"""🔄 {'Actif' if status['running'] else 'Inactif'}

📅 Prochaine génération:
{status['next_generation']}

📊 Cette semaine:
{stats['this_week']}/{stats['target_per_week']} leçons

📚 Total auto: {stats['total_auto']}"""
        
        self.scheduler_status.config(text=status_text)
        
        # Rafraîchir toutes les 60 secondes
        self.root.after(60000, self._update_scheduler_status)


def main():
    """Point d'entrée principal"""
    root = tk.Tk()
    app = MedicalGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
