"""
AI Agent Backend with Advanced Streaming and Progressive Responses
Handles all interactions with the OpenAI API with streaming support
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from config import DEFAULT_SETTINGS, AVAILABLE_MODELS

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Import trading context provider
try:
    from trading_context import TradingContextProvider
    TRADING_CONTEXT_AVAILABLE = True
except ImportError:
    TRADING_CONTEXT_AVAILABLE = False
    print("⚠️ Trading context non disponible")


class AIAgent:
    """
    Advanced AI Agent with streaming and progressive responses
    """
    
    def __init__(self, api_key=None, enable_trading_context=True):
        """Initialize the AI Agent"""
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Please set it in .env file or environment variables."
            )
        
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
        self.model = DEFAULT_SETTINGS["model"]
        self.temperature = DEFAULT_SETTINGS["temperature"]
        self.max_tokens = DEFAULT_SETTINGS["max_tokens"]
        
        # Advanced response parameters
        self.response_style = "balanced"  # "concise", "detailed", "balanced", "creative"
        self.detail_level = "medium"      # "brief", "medium", "comprehensive"
        self.language = "fr"              # Language for responses
        self.tone = "professional"        # "professional", "casual", "academic", "friendly"
        
        # Trading context integration
        self.trading_context_enabled = enable_trading_context and TRADING_CONTEXT_AVAILABLE
        self.trading_context_provider = None
        if self.trading_context_enabled:
            try:
                self.trading_context_provider = TradingContextProvider()
                print("🧠 Contexte de trading activé - L'agent connaît ses performances")
            except Exception as e:
                print(f"⚠️ Erreur activation contexte trading: {e}")
                self.trading_context_enabled = False
        
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self):
        """Build system prompt based on current parameters"""
        style_guide = {
            "concise": "Répondez de manière brève et directe.",
            "detailed": "Fournissez des réponses complètes et détaillées.",
            "balanced": "Équilibrez la concision et la profondeur.",
            "creative": "Soyez créatif et explorez différentes perspectives.",
        }
        
        detail_guide = {
            "brief": "Minimum de détails, juste les essentiels.",
            "medium": "Incluez les détails pertinents.",
            "comprehensive": "Explorez tous les aspects pertinents.",
        }
        
        tone_guide = {
            "professional": "Utilisez un ton professionnel et formel.",
            "casual": "Adoptez un ton décontracté et amical.",
            "academic": "Utilisez un ton académique et structuré.",
            "friendly": "Soyez chaleureux et approchable.",
        }
        
        base_prompt = f"""Tu es un assistant IA hautement capable et intelligent.
{style_guide.get(self.response_style, style_guide["balanced"])}
{detail_guide.get(self.detail_level, detail_guide["medium"])}
{tone_guide.get(self.tone, tone_guide["professional"])}
Réponds toujours en {self.language}.
Sois précis, utile et clair."""

        # Ajouter le contexte de trading si disponible
        if self.trading_context_enabled and self.trading_context_provider:
            try:
                trading_context = self.trading_context_provider.format_context_for_prompt()
                base_prompt = f"""{base_prompt}

---

🤖 CONTEXTE SPÉCIAL: TU ES UN AGENT DE TRADING AUTONOME

Tu n'es pas juste un assistant - tu es un agent de trading automatique qui 
prend des décisions d'investissement en temps réel.

{trading_context}

COMPORTEMENT ATTENDU:
- Quand on te demande "comment tu vas" ou "comment ça se passe", parle de tes trades
- Explique tes décisions avec tes vraies données ci-dessus
- Analyse tes erreurs honnêtement
- Discute de ton apprentissage en cours
- Donne des chiffres précis depuis tes fichiers
- Parle à la première personne ("j'ai tradé", "j'ai appris", "ma performance")

Ne dis JAMAIS "je n'ai pas accès aux données" - tu les as ci-dessus !
"""
            except Exception as e:
                print(f"⚠️ Erreur ajout contexte trading au prompt: {e}")
        
        return base_prompt
    
    def refresh_trading_context(self):
        """Rafraîchit le contexte de trading avec les dernières données"""
        if self.trading_context_enabled and self.trading_context_provider:
            try:
                self.system_prompt = self._build_system_prompt()
                return True
            except Exception as e:
                print(f"⚠️ Erreur rafraîchissement contexte: {e}")
                return False
        return False
    
    def send_message(self, user_message, use_streaming=False, callback=None, files_data=None):
        """
        Send a message to the AI and get a response
        
        Args:
            user_message (str): The user's input message
            use_streaming (bool): If True, use streaming for progressive responses
            callback (callable): Function to call with each chunk (for streaming)
            files_data (dict): Optional files data with images for vision API
            
        Returns:
            str: The complete AI response
        """
        # Rafraîchir le contexte de trading avant chaque message
        if self.trading_context_enabled:
            self.refresh_trading_context()
        
        # Allow sending if there's a message or files
        if not user_message and not files_data:
            raise ValueError("Message or files required")
        
        # Build message content with optional images
        content = self._build_message_content(user_message, files_data)
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": content
        })
        
        try:
            if use_streaming and callback:
                return self._send_message_streaming(callback)
            else:
                return self._send_message_regular()
            
        except OpenAIError as e:
            # Remove the failed user message from history
            self.conversation_history.pop()
            raise e
    
    def _build_message_content(self, user_message, files_data):
        """
        Build message content with text, images, and file content
        
        Includes:
        - User's text message
        - Images from files (for Vision API)
        - Transcribed audio content
        - Video descriptions
        - All readable file content
        """
        if not files_data:
            # Simple text message
            return user_message or "Veuillez analyser le fichier joint."
        
        # Build content list for API
        content = []
        
        # Add user's message or default
        if user_message:
            message_text = user_message
        else:
            message_text = "Veuillez analyser et discuter les fichiers suivants:"
        
        # Append all transcribed/processed content to message
        if files_data.get('text_content'):
            message_text += "\n\n" + "\n".join(files_data['text_content'])
        
        content.append({
            "type": "text",
            "text": message_text
        })
        
        # Add images for vision API (extracted from images and videos)
        if files_data.get('images'):
            content.extend(files_data['images'])
        
        return content
    
    def _send_message_regular(self):
        """Regular non-streaming API call"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def _send_message_streaming(self, callback):
        """Streaming API call with progressive response"""
        full_response = ""
        
        with self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True,  # Enable streaming
        ) as stream:
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    delta_text = chunk.choices[0].delta.content
                    full_response += delta_text
                    
                    # Call callback with each chunk for UI update
                    if callback:
                        try:
                            callback(delta_text)
                        except Exception as e:
                            print(f"Callback error: {e}")
        
        # Add complete response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": full_response
        })
        
        return full_response
    
    def set_response_style(self, style):
        """Change response style"""
        valid_styles = ["concise", "detailed", "balanced", "creative"]
        if style not in valid_styles:
            raise ValueError(f"Style must be one of: {valid_styles}")
        self.response_style = style
        self.system_prompt = self._build_system_prompt()
    
    def set_detail_level(self, level):
        """Change detail level"""
        valid_levels = ["brief", "medium", "comprehensive"]
        if level not in valid_levels:
            raise ValueError(f"Level must be one of: {valid_levels}")
        self.detail_level = level
        self.system_prompt = self._build_system_prompt()
    
    def set_language(self, language):
        """Change response language"""
        self.language = language
        self.system_prompt = self._build_system_prompt()
    
    def set_tone(self, tone):
        """Change response tone"""
        valid_tones = ["professional", "casual", "academic", "friendly"]
        if tone not in valid_tones:
            raise ValueError(f"Tone must be one of: {valid_tones}")
        self.tone = tone
        self.system_prompt = self._build_system_prompt()
    
    def set_model(self, model_name):
        """Change the AI model"""
        if model_name not in AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} not available. Choose from: {AVAILABLE_MODELS}")
        self.model = model_name
    
    def set_temperature(self, temperature):
        """Set temperature (0-2, higher = more creative)"""
        if not 0 <= temperature <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        self.temperature = temperature
    
    def set_max_tokens(self, max_tokens):
        """Set maximum tokens in response"""
        if max_tokens < 10:
            raise ValueError("Max tokens must be at least 10")
        self.max_tokens = max_tokens
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_model(self):
        """Get current model"""
        return self.model
    
    def get_conversation_length(self):
        """Get number of messages in conversation"""
        return len(self.conversation_history)
    
    def get_advanced_settings(self):
        """Get all advanced settings"""
        return {
            "response_style": self.response_style,
            "detail_level": self.detail_level,
            "language": self.language,
            "tone": self.tone,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
    
    def summarize_conversation(self):
        """Generate a summary of the conversation"""
        if len(self.conversation_history) < 2:
            return "Conversation trop courte pour un résumé."
        
        summary_prompt = f"""Résume cette conversation en 2-3 phrases clés:
{self._conversation_text()}"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.5,
            max_tokens=200,
        )
        
        return response.choices[0].message.content
    
    def _conversation_text(self):
        """Convert conversation history to readable text"""
        text = ""
        for msg in self.conversation_history:
            role = "Utilisateur" if msg["role"] == "user" else "Agent"
            text += f"\n{role}: {msg['content'][:200]}..."  # Limit for context
        return text
