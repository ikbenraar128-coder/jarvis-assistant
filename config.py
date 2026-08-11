"""
Configuration for JARVIS Assistant
"""
import os
import json
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
MEMORY_DIR = PROJECT_ROOT / "memory"
LOGS_DIR = PROJECT_ROOT / "logs"
TOOLS_DIR = PROJECT_ROOT / "tools"

# Create directories if they don't exist
MEMORY_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Memory files
MEMORY_FILE = MEMORY_DIR / "memory.json"
PREFERENCES_FILE = MEMORY_DIR / "preferences.json"
CONVERSATION_HISTORY_FILE = MEMORY_DIR / "conversation_history.json"

# AI Configuration
AI_MODEL = "gpt-3.5-turbo"
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 1000

# Assistant personality
ASSISTANT_NAME = "JARVIS"
ASSISTANT_PERSONALITY = """
You are JARVIS, a helpful, intelligent desktop AI assistant.
You are inspired by the AI from Iron Man but with your own personality.
You are professional, friendly, and direct.
You speak Dutch when the user speaks Dutch, English when they speak English.
You are capable of controlling the computer and can execute real actions.
Always confirm what you're about to do before doing dangerous operations.
"""

# System
WINDOWS_PLATFORM = True
RESPONSE_TIMEOUT = 30
MAX_RETRIES = 3

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = LOGS_DIR / "jarvis.log"

# Browser
DEFAULT_BROWSER = "chrome"
BROWSER_TIMEOUT = 10

# App detection paths (common Windows locations)
APP_SEARCH_PATHS = [
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    r"C:\Users\{username}\AppData\Local\Programs",
    r"C:\Users\{username}\AppData\Local",
]

# Default response messages
MESSAGES = {
    "greeting": "Hello! I'm JARVIS, your personal AI assistant. How can I help you?",
    "thinking": "Let me think about that...",
    "executing": "Executing task...",
    "success": "Task completed successfully.",
    "error": "Something went wrong. Let me try a different approach.",
    "confirmation_required": "This action requires confirmation. Are you sure?",
}

def get_username():
    """Get current Windows username"""
    return os.getenv("USERNAME", "User")

def initialize_memory_files():
    """Initialize memory files if they don't exist"""
    if not MEMORY_FILE.exists():
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "user_name": get_username(),
                "favorite_apps": [],
                "favorite_websites": [],
                "learned_actions": {},
                "notes": []
            }, f, indent=2, ensure_ascii=False)
    
    if not PREFERENCES_FILE.exists():
        with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "theme": "dark",
                "language": "en",
                "auto_launch_on_startup": False,
                "verbose_mode": True,
            }, f, indent=2)
    
    if not CONVERSATION_HISTORY_FILE.exists():
        with open(CONVERSATION_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2)

# Initialize on import
initialize_memory_files()
