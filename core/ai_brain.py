"""
AI Brain for JARVIS
Handles intent detection and natural language understanding
"""
import re
import json
from typing import Dict, List, Tuple
from enum import Enum

from core.memory_manager import memory_manager


class IntentType(Enum):
    """Types of intents the AI can understand"""
    CONVERSATION = "conversation"
    OPEN_APP = "open_app"
    CLOSE_APP = "close_app"
    OPEN_WEBSITE = "open_website"
    SEARCH_WEB = "search_web"
    OPEN_FOLDER = "open_folder"
    OPEN_FILE = "open_file"
    REMEMBER = "remember"
    RECALL = "recall"
    FORGET = "forget"
    EXECUTE_ACTION = "execute_action"
    SYSTEM_COMMAND = "system_command"
    MULTIPLE = "multiple"


class IntentResult:
    """Result of intent detection"""
    
    def __init__(self, intent_type: IntentType, confidence: float, 
                 data: Dict = None, original_text: str = ""):
        self.intent_type = intent_type
        self.confidence = confidence
        self.data = data or {}
        self.original_text = original_text


class AIBrain:
    """
    Core AI brain for JARVIS
    Detects user intent and generates appropriate responses
    """
    
    # Intent detection patterns
    INTENT_PATTERNS = {
        IntentType.OPEN_APP: [
            r'open\s+(\w+)',
            r'start\s+(\w+)',
            r'launch\s+(\w+)',
            r'run\s+(\w+)',
            r'execute\s+(\w+)',
        ],
        IntentType.CLOSE_APP: [
            r'close\s+(\w+)',
            r'stop\s+(\w+)',
            r'quit\s+(\w+)',
            r'exit\s+(\w+)',
            r'shut down\s+(\w+)',
        ],
        IntentType.OPEN_WEBSITE: [
            r'open\s+([\w.]+\.com|[\w.]+\.org|[\w.]+\.net)',
            r'go to\s+([\w.]+\.com|[\w.]+\.org|[\w.]+\.net)',
            r'visit\s+([\w.]+\.com|[\w.]+\.org|[\w.]+\.net)',
            r'browse\s+([\w.]+\.com|[\w.]+\.org|[\w.]+\.net)',
        ],
        IntentType.SEARCH_WEB: [
            r'search\s+(?:on\s+)?(?:google\s+)?(?:for\s+)?(.+)',
            r'find\s+(.+)',
            r'look up\s+(.+)',
            r'google\s+(.+)',
        ],
        IntentType.OPEN_FOLDER: [
            r'open\s+(?:my\s+)?(\w+)\s+(?:folder|directory)',
            r'show\s+(?:me\s+)?(?:my\s+)?(\w+)',
        ],
        IntentType.REMEMBER: [
            r'remember\s+(?:that\s+)?(.+)',
            r'remember\s+my\s+(.+)',
            r'note\s+(?:that\s+)?(.+)',
            r'save\s+(?:this\s+)?(.+)',
        ],
        IntentType.RECALL: [
            r"(?:what'?s?|do you know)\s+(?:my\s+)?(\w+)",
            r'do you remember\s+(.+)',
            r'recall\s+(.+)',
            r'who am i',
            r'what is my\s+(\w+)',
        ],
        IntentType.FORGET: [
            r'forget\s+(?:that\s+)?(.+)',
            r'forget\s+my\s+(.+)',
            r'delete\s+(?:my\s+)?(.+)',
            r'clear\s+(?:my\s+)?(.+)',
        ],
    }
    
    def __init__(self):
        self.memory = memory_manager
        self.conversation_context = []
    
    def detect_intent(self, user_input: str) -> IntentResult:
        """
        Detect user intent from input
        
        Args:
            user_input: User's text input
        
        Returns:
            IntentResult with detected intent and data
        """
        user_input_lower = user_input.lower().strip()
        
        # Check for multiple intents
        if self._is_multi_intent(user_input_lower):
            return IntentResult(
                IntentType.MULTIPLE,
                0.9,
                {"tasks": self._split_multi_tasks(user_input)},
                user_input
            )
        
        # Check each intent type
        for intent_type, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, user_input_lower, re.IGNORECASE)
                if match:
                    # Extract data from regex groups
                    data = {}
                    if match.groups():
                        data["target"] = match.group(1)
                    
                    return IntentResult(
                        intent_type,
                        0.85,
                        data,
                        user_input
                    )
        
        # Default to conversation
        return IntentResult(
            IntentType.CONVERSATION,
            0.5,
            {"message": user_input},
            user_input
        )
    
    def _is_multi_intent(self, text: str) -> bool:
        """Check if user input contains multiple tasks"""
        multi_indicators = [
            ' and ',
            ' then ',
            ' after that ',
            ', ',
            'and then',
            'after',
        ]
        return any(indicator in text for indicator in multi_indicators)
    
    def _split_multi_tasks(self, text: str) -> List[str]:
        """Split multi-intent text into individual tasks"""
        tasks = re.split(r'(?:,\s*|\band\s+|\bthen\s+|\bafter\s+)', text)
        return [task.strip() for task in tasks if task.strip()]
    
    def generate_response(self, intent: IntentResult, execution_result: Dict = None) -> str:
        """
        Generate appropriate response based on intent
        
        Args:
            intent: Detected intent
            execution_result: Result from executing the task
        
        Returns:
            Response string
        """
        if intent.intent_type == IntentType.OPEN_APP:
            app_name = intent.data.get("target", "")
            if execution_result and execution_result.get("success"):
                return f"✓ {app_name} is now open."
            return f"Opening {app_name}..."
        
        elif intent.intent_type == IntentType.CLOSE_APP:
            app_name = intent.data.get("target", "")
            if execution_result and execution_result.get("success"):
                return f"✓ {app_name} closed."
            return f"Closing {app_name}..."
        
        elif intent.intent_type == IntentType.OPEN_WEBSITE:
            website = intent.data.get("target", "")
            if execution_result and execution_result.get("success"):
                return f"✓ Opening {website}."
            return f"Opening {website}..."
        
        elif intent.intent_type == IntentType.SEARCH_WEB:
            query = intent.data.get("target", "")
            if execution_result and execution_result.get("success"):
                return f"✓ Search for '{query}' is ready."
            return f"Searching for '{query}'..."
        
        elif intent.intent_type == IntentType.REMEMBER:
            content = intent.data.get("target", "")
            if execution_result and execution_result.get("success"):
                return f"✓ I'll remember that: {content}"
            return f"Saving to memory: {content}"
        
        elif intent.intent_type == IntentType.RECALL:
            if execution_result and execution_result.get("success"):
                recalled = execution_result.get("data", "")
                return f"I recall: {recalled}"
            return "Let me check my memory..."
        
        elif intent.intent_type == IntentType.CONVERSATION:
            return "I'm listening. Tell me more..."
        
        else:
            return "Processing your request..."
    
    def add_to_context(self, role: str, message: str):
        """Add message to conversation context"""
        self.conversation_context.append({"role": role, "message": message})
        # Keep context limited to last 10 messages
        if len(self.conversation_context) > 10:
            self.conversation_context.pop(0)
    
    def get_context(self) -> str:
        """Get conversation context as string"""
        context_str = ""
        for entry in self.conversation_context:
            context_str += f"{entry['role']}: {entry['message']}\n"
        return context_str
