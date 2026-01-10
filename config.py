"""
Configuration module for the AI Agent
Manages all settings for UI themes, fonts, and API configuration
"""

# ============ THEMES ============
THEMES = {
    "light": {
        "bg_main": "#f5f5f5",
        "bg_secondary": "#ffffff",
        "text_main": "#1a1a1a",
        "text_secondary": "#555555",
        "accent": "#0066cc",
        "accent_hover": "#0052a3",
        "border": "#cccccc",
        "user_bubble": "#0066cc",
        "user_text": "#ffffff",
        "agent_bubble": "#e8e8e8",
        "agent_text": "#1a1a1a",
    },
    "dark": {
        "bg_main": "#1e1e1e",
        "bg_secondary": "#2d2d2d",
        "text_main": "#ffffff",
        "text_secondary": "#b0b0b0",
        "accent": "#00a8ff",
        "accent_hover": "#0088cc",
        "border": "#444444",
        "user_bubble": "#0066cc",
        "user_text": "#ffffff",
        "agent_bubble": "#3a3a3a",
        "agent_text": "#e0e0e0",
    }
}

# ============ DEFAULT SETTINGS ============
DEFAULT_SETTINGS = {
    "theme": "dark",
    "font_size": 11,
    "font_family": "Segoe UI",
    "auto_scroll": True,
    "show_timestamps": False,
    "model": "gpt-4o-mini",
    "max_tokens": 2000,
    "temperature": 0.7,
}

# ============ FONT SIZES ============
FONT_SIZES = {
    "small": 9,
    "normal": 11,
    "large": 13,
    "xl": 15,
}

# ============ MODELS ============
AVAILABLE_MODELS = [
    "gpt-4o-mini",
    "gpt-4",
    "gpt-3.5-turbo",
]

# ============ UI DIMENSIONS ============
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 500

# ============ BUTTON STYLE ============
BUTTON_STYLES = {
    "send_button": {
        "padx": 20,
        "pady": 12,
        "font_size_offset": 2,
        "relief": "flat",
    }
}
