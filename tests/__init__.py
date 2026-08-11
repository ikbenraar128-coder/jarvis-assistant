"""
Tests for JARVIS
"""
import pytest
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ai_brain import AIBrain, IntentType
from core.task_planner import TaskPlanner
from core.memory_manager import MemoryManager


class TestAIBrain:
    """Tests for AI Brain"""
    
    def setup_method(self):
        self.brain = AIBrain()
    
    def test_intent_open_app(self):
        """Test detecting open app intent"""
        intent = self.brain.detect_intent("open chrome")
        assert intent.intent_type == IntentType.OPEN_APP
        assert "chrome" in intent.data.get("target", "").lower()
    
    def test_intent_close_app(self):
        """Test detecting close app intent"""
        intent = self.brain.detect_intent("close firefox")
        assert intent.intent_type == IntentType.CLOSE_APP
        assert "firefox" in intent.data.get("target", "").lower()
    
    def test_intent_search(self):
        """Test detecting search intent"""
        intent = self.brain.detect_intent("search for python tutorial")
        assert intent.intent_type == IntentType.SEARCH_WEB
    
    def test_intent_remember(self):
        """Test detecting remember intent"""
        intent = self.brain.detect_intent("remember my name is John")
        assert intent.intent_type == IntentType.REMEMBER
    
    def test_intent_recall(self):
        """Test detecting recall intent"""
        intent = self.brain.detect_intent("what's my name")
        assert intent.intent_type == IntentType.RECALL
    
    def test_multi_intent(self):
        """Test detecting multiple intents"""
        intent = self.brain.detect_intent("open chrome and search for python")
        assert intent.intent_type == IntentType.MULTIPLE
        assert len(intent.data.get("tasks", [])) > 1


class TestTaskPlanner:
    """Tests for Task Planner"""
    
    def setup_method(self):
        self.brain = AIBrain()
        self.planner = TaskPlanner()
    
    def test_plan_open_app(self):
        """Test planning to open app"""
        intent = self.brain.detect_intent("open notepad")
        plan = self.planner.plan_task(intent)
        
        assert len(plan.steps) > 0
        assert plan.steps[0].action == "check_app_running"
    
    def test_plan_search(self):
        """Test planning to search"""
        intent = self.brain.detect_intent("search python")
        plan = self.planner.plan_task(intent)
        
        assert len(plan.steps) > 0
        assert any(step.action == "search_web" for step in plan.steps)
    
    def test_plan_multiple_tasks(self):
        """Test planning multiple tasks"""
        intent = self.brain.detect_intent("open chrome and search google")
        plan = self.planner.plan_task(intent)
        
        assert len(plan.steps) > 0


class TestMemoryManager:
    """Tests for Memory Manager"""
    
    def setup_method(self):
        self.memory = MemoryManager()
    
    def test_remember_and_recall(self):
        """Test remembering and recalling"""
        self.memory.remember("test_key", "test_value")
        recalled = self.memory.recall("test_key")
        assert recalled == "test_value"
    
    def test_forget(self):
        """Test forgetting"""
        self.memory.remember("test_key", "test_value")
        self.memory.forget("test_key")
        recalled = self.memory.recall("test_key")
        assert recalled is None
    
    def test_add_favorite_app(self):
        """Test adding favorite app"""
        self.memory.add_favorite_app("Chrome")
        apps = self.memory.get_favorite_apps()
        assert "Chrome" in apps
    
    def test_conversation_history(self):
        """Test conversation history"""
        self.memory.add_to_history("user", "Hello")
        self.memory.add_to_history("assistant", "Hi there!")
        
        history = self.memory.get_history()
        assert len(history) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
