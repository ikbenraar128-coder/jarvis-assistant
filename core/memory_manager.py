"""
Memory management system for JARVIS
Handles persistent storage of user data and preferences
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

from config import (
    MEMORY_FILE, 
    PREFERENCES_FILE, 
    CONVERSATION_HISTORY_FILE
)


class MemoryManager:
    """Manages persistent memory and preferences"""
    
    def __init__(self):
        self.memory_file = MEMORY_FILE
        self.preferences_file = PREFERENCES_FILE
        self.history_file = CONVERSATION_HISTORY_FILE
        self.memory = self._load_memory()
        self.preferences = self._load_preferences()
        self.history = self._load_history()
    
    def _load_memory(self) -> Dict:
        """Load memory from file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading memory: {e}")
        return {}
    
    def _load_preferences(self) -> Dict:
        """Load preferences from file"""
        try:
            if self.preferences_file.exists():
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading preferences: {e}")
        return {}
    
    def _load_history(self) -> List:
        """Load conversation history from file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
        return []
    
    def _save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def _save_preferences(self):
        """Save preferences to file"""
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    def _save_history(self):
        """Save conversation history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    # ========== MEMORY OPERATIONS ==========
    
    def remember(self, key: str, value: Any, category: str = "general"):
        """
        Store information in memory
        
        Args:
            key: Memory key
            value: Value to store
            category: Memory category
        """
        if category not in self.memory:
            self.memory[category] = {}
        
        self.memory[category][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save_memory()
    
    def recall(self, key: str, category: str = "general") -> Optional[Any]:
        """
        Retrieve information from memory
        
        Args:
            key: Memory key
            category: Memory category
        
        Returns:
            Value if found, None otherwise
        """
        if category in self.memory and key in self.memory[category]:
            return self.memory[category][key].get("value")
        return None
    
    def forget(self, key: str, category: str = "general") -> bool:
        """
        Delete information from memory
        
        Args:
            key: Memory key
            category: Memory category
        
        Returns:
            True if deleted, False if not found
        """
        if category in self.memory and key in self.memory[category]:
            del self.memory[category][key]
            self._save_memory()
            return True
        return False
    
    def update_memory(self, key: str, value: Any, category: str = "general"):
        """Update existing memory entry"""
        self.remember(key, value, category)
    
    def get_all_memory(self, category: str = None) -> Dict:
        """Get all memory from a category or all categories"""
        if category:
            return self.memory.get(category, {})
        return self.memory
    
    # ========== PREFERENCE OPERATIONS ==========
    
    def set_preference(self, key: str, value: Any):
        """Set a preference"""
        self.preferences[key] = value
        self._save_preferences()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a preference"""
        return self.preferences.get(key, default)
    
    # ========== CONVERSATION HISTORY ==========
    
    def add_to_history(self, role: str, message: str, metadata: Dict = None):
        """
        Add message to conversation history
        
        Args:
            role: "user" or "assistant"
            message: Message content
            metadata: Additional metadata
        """
        entry = {
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.history.append(entry)
        self._save_history()
    
    def get_history(self, limit: int = 50) -> List:
        """Get conversation history (last N entries)"""
        return self.history[-limit:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.history = []
        self._save_history()
    
    # ========== FAVORITE APPS & WEBSITES ==========
    
    def add_favorite_app(self, app_name: str):
        """Add app to favorites"""
        if "favorite_apps" not in self.memory:
            self.memory["favorite_apps"] = []
        
        if app_name not in self.memory["favorite_apps"]:
            self.memory["favorite_apps"].append(app_name)
            self._save_memory()
    
    def get_favorite_apps(self) -> List[str]:
        """Get favorite apps"""
        return self.memory.get("favorite_apps", [])
    
    def remove_favorite_app(self, app_name: str):
        """Remove app from favorites"""
        if "favorite_apps" in self.memory and app_name in self.memory["favorite_apps"]:
            self.memory["favorite_apps"].remove(app_name)
            self._save_memory()
    
    def add_favorite_website(self, website_url: str, name: str = None):
        """Add website to favorites"""
        if "favorite_websites" not in self.memory:
            self.memory["favorite_websites"] = []
        
        entry = {"url": website_url, "name": name or website_url}
        
        if entry not in self.memory["favorite_websites"]:
            self.memory["favorite_websites"].append(entry)
            self._save_memory()
    
    def get_favorite_websites(self) -> List[Dict]:
        """Get favorite websites"""
        return self.memory.get("favorite_websites", [])


# Global instance
memory_manager = MemoryManager()
